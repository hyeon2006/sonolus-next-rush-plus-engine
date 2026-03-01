import { type LevelData, type LevelDataEntity } from '@sonolus/core'

type ExtendedEntityDataField = {
    name: string
    value?: number
    ref?: string
}

export type ExtendedEntityData = {
    archetype: string
    name?: string
    data: ExtendedEntityDataField[]
}

export type ExtendedLevelData = {
    bgmOffset: number
    entities: ExtendedEntityData[]
}

type FlatData = Record<string, number | string>

type FlatEntity = {
    archetype: string
    name?: string
    data: FlatData
}

type IntermediateEntity = {
    archetype: string
    data: Record<string, number | IntermediateEntity>
}

const ConnectorKind = {
    ACTIVE_NORMAL: 1,
    ACTIVE_CRITICAL: 2,
    GUIDE_NEUTRAL: 101,
    GUIDE_RED: 102,
    GUIDE_GREEN: 103,
    GUIDE_BLUE: 104,
    GUIDE_YELLOW: 105,
    GUIDE_PURPLE: 106,
    GUIDE_CYAN: 107,
    GUIDE_BLACK: 108,
} as const

const FlickDirection = {
    UP_OMNI: 0,
    UP_LEFT: 1,
    UP_RIGHT: 2,
} as const

const EaseType = {
    LINEAR: 1,
    IN_QUAD: 2,
    OUT_QUAD: 3,
    IN_OUT_QUAD: 4,
    OUT_IN_QUAD: 5,
} as const

const noteTypeMapping: Record<string, string> = {
    NormalTapNote: 'NormalTapNote',
    CriticalTapNote: 'CriticalTapNote',
    NormalFlickNote: 'NormalFlickNote',
    CriticalFlickNote: 'CriticalFlickNote',
    NormalSlideStartNote: 'NormalHeadTapNote',
    CriticalSlideStartNote: 'CriticalHeadTapNote',
    NormalSlideEndNote: 'NormalTailReleaseNote',
    CriticalSlideEndNote: 'CriticalTailReleaseNote',
    NormalSlideEndFlickNote: 'NormalTailFlickNote',
    CriticalSlideEndFlickNote: 'CriticalTailFlickNote',
    IgnoredSlideTickNote: 'TransientHiddenTickNote',
    NormalSlideTickNote: 'NormalTickNote',
    CriticalSlideTickNote: 'CriticalTickNote',
    HiddenSlideTickNote: 'AnchorNote',
    NormalAttachedSlideTickNote: 'NormalTickNote',
    CriticalAttachedSlideTickNote: 'CriticalTickNote',
    NormalTraceNote: 'NormalTraceNote',
    CriticalTraceNote: 'CriticalTraceNote',
    DamageNote: 'DamageNote',
    NormalTraceFlickNote: 'NormalTraceFlickNote',
    CriticalTraceFlickNote: 'CriticalTraceFlickNote',
    NonDirectionalTraceFlickNote: 'NormalTraceFlickNote',
    HiddenSlideStartNote: 'AnchorNote',
    NormalTraceSlideStartNote: 'NormalHeadTraceNote',
    CriticalTraceSlideStartNote: 'CriticalHeadTraceNote',
    NormalTraceSlideEndNote: 'NormalTailTraceNote',
    CriticalTraceSlideEndNote: 'CriticalTailTraceNote',
}

const activeConnectorKindMapping: Record<string, number> = {
    NormalSlideConnector: ConnectorKind.ACTIVE_NORMAL,
    CriticalSlideConnector: ConnectorKind.ACTIVE_CRITICAL,
}

const flickDirectionMapping: Record<number, number> = {
    [-1]: FlickDirection.UP_LEFT,
    0: FlickDirection.UP_OMNI,
    1: FlickDirection.UP_RIGHT,
}

const easeTypeMapping: Record<number, number> = {
    [-2]: EaseType.OUT_IN_QUAD,
    [-1]: EaseType.OUT_QUAD,
    0: EaseType.LINEAR,
    1: EaseType.IN_QUAD,
    2: EaseType.IN_OUT_QUAD,
}

const fadeAlphaMapping: Record<number, [number, number]> = {
    0: [1.0, 0.0],
    1: [1.0, 1.0],
    2: [0.0, 1.0],
}

const guideKindMapping: Record<number, number> = {
    0: ConnectorKind.GUIDE_NEUTRAL,
    1: ConnectorKind.GUIDE_RED,
    2: ConnectorKind.GUIDE_GREEN,
    3: ConnectorKind.GUIDE_BLUE,
    4: ConnectorKind.GUIDE_YELLOW,
    5: ConnectorKind.GUIDE_PURPLE,
    6: ConnectorKind.GUIDE_CYAN,
    7: ConnectorKind.GUIDE_BLACK,
}

/** data 배열 → 평탄한 Record로 변환 (value → number, ref → string) */
const flattenData = (fields: ExtendedEntityDataField[]): FlatData => {
    const result: FlatData = {}
    for (const field of fields) {
        if (field.value !== undefined) result[field.name] = field.value
        else if (field.ref !== undefined) result[field.name] = field.ref
    }
    return result
}

/** 숫자 값 읽기 */
const getNum = (data: FlatData, key: string, defaultValue = 0): number => {
    const val = data[key]
    if (typeof val === 'number') return val
    if (typeof val === 'string') {
        const n = Number(val)
        return isNaN(n) ? defaultValue : n
    }
    return defaultValue
}

/** 참조 값 읽기 (number | string) */
const getEntityRef = (data: FlatData, key: string): number | string | undefined => {
    const val = data[key]
    if (val === undefined) return undefined
    return val
}

/** 참조로 FlatEntity 조회 (number → 인덱스, string → 이름) */
const resolveEntity = (
    ref: number | string,
    entities: FlatEntity[],
    entitiesByName: Map<string, FlatEntity>,
): FlatEntity | undefined => {
    if (typeof ref === 'number') return entities[ref]
    return entitiesByName.get(ref)
}

/** Convert a PJSekaiExtendedLevelData to a Level Data (Next Sekai) */
export const extendedToLevelData = (data: ExtendedLevelData, offset = 0): LevelData => {
    const flatEntities: FlatEntity[] = data.entities.map((e) => ({
        archetype: e.archetype,
        name: e.name,
        data: flattenData(e.data),
    }))

    const entitiesByName = new Map<string, FlatEntity>()
    for (const entity of flatEntities) {
        if (entity.name) entitiesByName.set(entity.name, entity)
    }

    const resolve = (ref: number | string | undefined): FlatEntity | undefined => {
        if (ref === undefined) return undefined
        return resolveEntity(ref, flatEntities, entitiesByName)
    }

    const allIntermediateEntities: IntermediateEntity[] = []

    const createIntermediate = (
        archetype: string,
        entityData: Record<string, number | IntermediateEntity>,
    ): IntermediateEntity => {
        const entity: IntermediateEntity = { archetype, data: entityData }
        allIntermediateEntities.push(entity)
        return entity
    }

    createIntermediate('Initialization', {})

    for (const entity of flatEntities) {
        if (entity.archetype !== '#BPM_CHANGE') continue
        createIntermediate('#BPM_CHANGE', {
            '#BEAT': getNum(entity.data, '#BEAT'),
            '#BPM': getNum(entity.data, '#BPM'),
        })
    }

    const timescaleGroupsByIndex = new Map<number, IntermediateEntity>()
    const timescaleGroupsByName = new Map<string, IntermediateEntity>()

    for (let i = 0; i < flatEntities.length; i++) {
        const entity = flatEntities[i]
        if (entity.archetype !== 'TimeScaleGroup') continue

        const groupIntermediate = createIntermediate('TimeScaleGroup', {})
        timescaleGroupsByIndex.set(i, groupIntermediate)
        if (entity.name) timescaleGroupsByName.set(entity.name, groupIntermediate)

        let rawChangeRef = getEntityRef(entity.data, 'first')
        let lastChangeIntermediate: IntermediateEntity | null = null

        while (rawChangeRef !== undefined) {
            const rawChange = resolve(rawChangeRef)
            if (!rawChange) break

            const changeIntermediate = createIntermediate('TimeScaleChange', {
                '#BEAT': getNum(rawChange.data, '#BEAT'),
                timeScale: getNum(rawChange.data, 'timeScale'),
                timeScaleSkip: 0.0,
                timeScaleGroup: groupIntermediate,
                timeScaleEase: 0,
            })

            if (lastChangeIntermediate) {
                lastChangeIntermediate.data['next'] = changeIntermediate
            } else {
                groupIntermediate.data['first'] = changeIntermediate
            }
            lastChangeIntermediate = changeIntermediate

            rawChangeRef = getEntityRef(rawChange.data, 'next')
        }
    }

    const resolveTimescaleGroup = (
        ref: number | string | undefined,
    ): IntermediateEntity | undefined => {
        if (ref === undefined) return undefined
        if (typeof ref === 'number') return timescaleGroupsByIndex.get(ref)
        return timescaleGroupsByName.get(ref)
    }

    const notesByIndex = new Map<number, IntermediateEntity>()
    const notesByName = new Map<string, IntermediateEntity>()

    for (let i = 0; i < flatEntities.length; i++) {
        const entity = flatEntities[i]
        const mappedArchetype = noteTypeMapping[entity.archetype]
        if (!mappedArchetype) continue

        const tsg = resolveTimescaleGroup(getEntityRef(entity.data, 'timeScaleGroup'))

        const noteData: Record<string, number | IntermediateEntity> = {
            '#BEAT': getNum(entity.data, '#BEAT'),
            lane: getNum(entity.data, 'lane', 0),
            size: getNum(entity.data, 'size', 0),
            direction: flickDirectionMapping[getNum(entity.data, 'direction', 0)],
            segmentKind: ConnectorKind.ACTIVE_NORMAL,
        }
        if (tsg !== undefined) noteData['#TIMESCALE_GROUP'] = tsg

        const noteIntermediate = createIntermediate(mappedArchetype, noteData)
        notesByIndex.set(i, noteIntermediate)
        if (entity.name) notesByName.set(entity.name, noteIntermediate)
    }

    const resolveNote = (ref: number | string | undefined): IntermediateEntity | undefined => {
        if (ref === undefined) return undefined
        if (typeof ref === 'number') return notesByIndex.get(ref)
        return notesByName.get(ref)
    }

    const connectorsByIndex = new Map<number, IntermediateEntity>()
    const connectorsByName = new Map<string, IntermediateEntity>()

    for (let i = 0; i < flatEntities.length; i++) {
        const entity = flatEntities[i]
        const connectorKind = activeConnectorKindMapping[entity.archetype]
        if (!connectorKind) continue

        const headNote = resolveNote(getEntityRef(entity.data, 'head'))
        const tailNote = resolveNote(getEntityRef(entity.data, 'tail'))
        const segmentHeadNote = resolveNote(getEntityRef(entity.data, 'start'))
        const segmentTailNote = resolveNote(getEntityRef(entity.data, 'end'))

        if (!headNote || !tailNote || !segmentHeadNote || !segmentTailNote) continue

        const connectorIntermediate = createIntermediate('Connector', {
            head: headNote,
            tail: tailNote,
            segmentHead: segmentHeadNote,
            segmentTail: segmentTailNote,
            activeHead: segmentHeadNote,
            activeTail: segmentTailNote,
        })

        headNote.data['connectorEase'] =
            easeTypeMapping[getNum(entity.data, 'ease', 0)] ?? EaseType.LINEAR
        headNote.data['segmentKind'] = connectorKind
        tailNote.data['segmentKind'] = connectorKind
        segmentHeadNote.data['segmentKind'] = connectorKind

        connectorsByIndex.set(i, connectorIntermediate)
        if (entity.name) connectorsByName.set(entity.name, connectorIntermediate)
    }

    const resolveConnector = (ref: number | string | undefined): IntermediateEntity | undefined => {
        if (ref === undefined) return undefined
        if (typeof ref === 'number') return connectorsByIndex.get(ref)
        return connectorsByName.get(ref)
    }

    for (let i = 0; i < flatEntities.length; i++) {
        const entity = flatEntities[i]
        const note = notesByIndex.get(i)
        if (!note) continue

        const attachRef = getEntityRef(entity.data, 'attach')
        if (attachRef !== undefined) {
            const attachConnector = resolveConnector(attachRef)
            if (attachConnector) {
                note.data['attachHead'] = attachConnector.data['head']
                note.data['attachTail'] = attachConnector.data['tail']
                note.data['isAttached'] = 1
            }
        }

        const slideRef = getEntityRef(entity.data, 'slide')
        if (slideRef !== undefined) {
            const slideConnector = resolveConnector(slideRef)
            if (slideConnector) {
                note.data['activeHead'] = slideConnector.data['activeHead']
            }
        }
    }

    for (const entity of flatEntities) {
        if (entity.archetype !== 'SimLine') continue
        const left = resolveNote(getEntityRef(entity.data, 'a'))
        const right = resolveNote(getEntityRef(entity.data, 'b'))
        if (left && right) createIntermediate('SimLine', { left, right })
    }

    const anchorsByBeat = new Map<number, IntermediateEntity[]>()
    const anchorPositions = new Map<IntermediateEntity, Set<string>>()

    const getAnchor = (
        beat: number,
        lane: number,
        size: number,
        tsg: IntermediateEntity | undefined,
        pos: 'segmentHead' | 'segmentTail' | 'head' | 'tail',
        segmentKind = -1,
        segmentAlpha = -1,
        connectorEase = -1,
    ): IntermediateEntity => {
        const anchors = anchorsByBeat.get(beat)
        if (anchors) {
            for (const anchor of anchors) {
                if (anchorPositions.get(anchor)?.has(pos)) continue
                if (
                    anchor.data['lane'] === lane &&
                    anchor.data['size'] === size &&
                    anchor.data['#TIMESCALE_GROUP'] === tsg &&
                    (segmentKind === -1 ||
                        anchor.data['segmentKind'] === segmentKind ||
                        anchor.data['segmentKind'] === -1) &&
                    (segmentAlpha === -1 ||
                        anchor.data['segmentAlpha'] === segmentAlpha ||
                        anchor.data['segmentAlpha'] === -1) &&
                    (connectorEase === -1 ||
                        anchor.data['connectorEase'] === connectorEase ||
                        anchor.data['connectorEase'] === -1)
                ) {
                    if (segmentKind !== -1 && anchor.data['segmentKind'] === -1)
                        anchor.data['segmentKind'] = segmentKind
                    if (segmentAlpha !== -1 && anchor.data['segmentAlpha'] === -1)
                        anchor.data['segmentAlpha'] = segmentAlpha
                    if (connectorEase !== -1 && anchor.data['connectorEase'] === -1)
                        anchor.data['connectorEase'] = connectorEase
                    anchorPositions.get(anchor)!.add(pos)
                    return anchor
                }
            }
        }

        const anchorData: Record<string, number | IntermediateEntity> = {
            '#BEAT': beat,
            lane,
            size,
            segmentKind,
            segmentAlpha,
            connectorEase,
        }
        if (tsg !== undefined) anchorData['#TIMESCALE_GROUP'] = tsg

        const anchor = createIntermediate('AnchorNote', anchorData)
        if (!anchorsByBeat.has(beat)) anchorsByBeat.set(beat, [])
        anchorsByBeat.get(beat)!.push(anchor)
        anchorPositions.set(anchor, new Set([pos]))
        return anchor
    }

    for (const entity of flatEntities) {
        if (entity.archetype !== 'Guide') continue

        const startBeat = getNum(entity.data, 'startBeat')
        const startLane = getNum(entity.data, 'startLane')
        const startSize = getNum(entity.data, 'startSize')
        const startTSG = resolveTimescaleGroup(getEntityRef(entity.data, 'startTimeScaleGroup'))

        const headBeat = getNum(entity.data, 'headBeat')
        const headLane = getNum(entity.data, 'headLane')
        const headSize = getNum(entity.data, 'headSize')
        const headTSG = resolveTimescaleGroup(getEntityRef(entity.data, 'headTimeScaleGroup'))

        const tailBeat = getNum(entity.data, 'tailBeat')
        const tailLane = getNum(entity.data, 'tailLane')
        const tailSize = getNum(entity.data, 'tailSize')
        const tailTSG = resolveTimescaleGroup(getEntityRef(entity.data, 'tailTimeScaleGroup'))

        const endBeat = getNum(entity.data, 'endBeat')
        const endLane = getNum(entity.data, 'endLane')
        const endSize = getNum(entity.data, 'endSize')
        const endTSG = resolveTimescaleGroup(getEntityRef(entity.data, 'endTimeScaleGroup'))

        const ease = easeTypeMapping[getNum(entity.data, 'ease', 0)] ?? EaseType.LINEAR
        const [startAlpha, endAlpha] = fadeAlphaMapping[getNum(entity.data, 'fade', 1)]
        const kind =
            guideKindMapping[getNum(entity.data, 'color', 0)] ?? ConnectorKind.GUIDE_NEUTRAL

        const start = getAnchor(
            startBeat,
            startLane,
            startSize,
            startTSG,
            'segmentHead',
            kind,
            startAlpha,
        )
        const end = getAnchor(endBeat, endLane, endSize, endTSG, 'segmentTail', kind, endAlpha)
        const head = getAnchor(headBeat, headLane, headSize, headTSG, 'head', kind, -1, ease)
        const tail = getAnchor(tailBeat, tailLane, tailSize, tailTSG, 'tail', kind)

        createIntermediate('Connector', { head, tail, segmentHead: start, segmentTail: end })
    }

    for (const anchorList of anchorsByBeat.values()) {
        for (const anchor of anchorList) {
            if (anchor.data['segmentKind'] === -1)
                anchor.data['segmentKind'] = ConnectorKind.GUIDE_NEUTRAL
            if (anchor.data['segmentAlpha'] === -1) anchor.data['segmentAlpha'] = 1.0
            if (anchor.data['connectorEase'] === -1) anchor.data['connectorEase'] = EaseType.LINEAR
        }
    }

    for (const entity of allIntermediateEntities) {
        if (entity.archetype !== 'Connector') continue
        const head = entity.data['head'] as IntermediateEntity
        const tail = entity.data['tail'] as IntermediateEntity
        if (head && tail) head.data['next'] = tail
    }

    allIntermediateEntities.sort((a, b) => {
        const isInitA = a.archetype === 'Initialization' ? 0 : 1
        const isInitB = b.archetype === 'Initialization' ? 0 : 1
        if (isInitA !== isInitB) return isInitA - isInitB
        const beatA = typeof a.data['#BEAT'] === 'number' ? a.data['#BEAT'] : -1
        const beatB = typeof b.data['#BEAT'] === 'number' ? b.data['#BEAT'] : -1
        return beatA - beatB
    })

    const entities: LevelDataEntity[] = []
    const intermediateToRef = new Map<IntermediateEntity, string>()
    let entityRefCounter = 0

    const getOutputRef = (intermediateEntity: IntermediateEntity): string => {
        let ref = intermediateToRef.get(intermediateEntity)
        if (ref !== undefined) return ref
        ref = (entityRefCounter++).toString(16)
        intermediateToRef.set(intermediateEntity, ref)
        return ref
    }

    for (const intermediateEntity of allIntermediateEntities) {
        const entity: LevelDataEntity = {
            archetype: intermediateEntity.archetype,
            name: getOutputRef(intermediateEntity),
            data: [],
        }

        for (const [dataName, dataValue] of Object.entries(intermediateEntity.data)) {
            if (typeof dataValue === 'number') {
                entity.data.push({ name: dataName, value: dataValue })
            } else if (dataValue !== undefined && dataValue !== null) {
                entity.data.push({
                    name: dataName,
                    ref: getOutputRef(dataValue as IntermediateEntity),
                })
            }
        }

        entities.push(entity)
    }

    return {
        bgmOffset: data.bgmOffset + offset,
        entities,
    }
}
