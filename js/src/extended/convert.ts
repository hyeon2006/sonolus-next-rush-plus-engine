import { type LevelData, type LevelDataEntity } from '@sonolus/core'

export type ExtendedEntityData = {
    archetype: string
    data: Record<string, number | string>
}

export type ExtendedLevelData = {
    bgmOffset: number
    entities: ExtendedEntityData[]
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

/** Convert a PJSekaiExtendedLevelData to a Level Data (Next Sekai) */
export const extendedToLevelData = (data: ExtendedLevelData, offset = 0): LevelData => {
    const allIntermediateEntities: IntermediateEntity[] = []

    const createIntermediate = (
        archetype: string,
        entityData: Record<string, number | IntermediateEntity>,
    ): IntermediateEntity => {
        const intermediateEntity: IntermediateEntity = { archetype, data: entityData }
        allIntermediateEntities.push(intermediateEntity)
        return intermediateEntity
    }

    createIntermediate('Initialization', {})

    for (const entity of data.entities) {
        if (entity.archetype === '#BPM_CHANGE') {
            createIntermediate('#BPM_CHANGE', {
                '#BEAT': entity.data['#BEAT'] as number,
                '#BPM': entity.data['#BPM'] as number,
            })
        }
    }

    const timescaleGroupsByIndex = new Map<number, IntermediateEntity>()
    for (let i = 0; i < data.entities.length; i++) {
        const entity = data.entities[i]
        if (entity.archetype === 'TimeScaleGroup') {
            const groupIntermediate = createIntermediate('TimeScaleGroup', {})
            timescaleGroupsByIndex.set(i, groupIntermediate)

            let rawChangeIdx = entity.data['first'] as number
            let lastChangeIntermediate: IntermediateEntity | null = null

            while (rawChangeIdx !== undefined && rawChangeIdx > 0) {
                const rawChange = data.entities[rawChangeIdx]
                const changeIntermediate = createIntermediate('TimeScaleChange', {
                    '#BEAT': rawChange.data['#BEAT'] as number,
                    timeScale: rawChange.data['timeScale'] as number,
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

                const nextIdx = rawChange.data['next'] as number
                if (nextIdx !== undefined && nextIdx > 0) {
                    rawChangeIdx = nextIdx
                } else {
                    break
                }
            }
        }
    }

    const notesByOriginalIndex = new Map<number, IntermediateEntity>()
    for (let i = 0; i < data.entities.length; i++) {
        const entity = data.entities[i]
        if (noteTypeMapping[entity.archetype]) {
            const mappedArchetype = noteTypeMapping[entity.archetype]
            const directionData = (entity.data['direction'] as number) ?? 0
            const noteIntermediate = createIntermediate(mappedArchetype, {
                '#BEAT': entity.data['#BEAT'] as number,
                lane: (entity.data['lane'] as number) ?? 0.0,
                size: (entity.data['size'] as number) ?? 0.0,
                direction: flickDirectionMapping[directionData],
                segmentKind: ConnectorKind.ACTIVE_NORMAL,
            })
            notesByOriginalIndex.set(i, noteIntermediate)
        }
    }

    const connectorsByOriginalIndex = new Map<number, IntermediateEntity>()
    for (let i = 0; i < data.entities.length; i++) {
        const entity = data.entities[i]
        if (activeConnectorKindMapping[entity.archetype]) {
            const connectorKind = activeConnectorKindMapping[entity.archetype]

            const head = notesByOriginalIndex.get(entity.data['head'] as number)
            const tail = notesByOriginalIndex.get(entity.data['tail'] as number)
            const segmentHead = notesByOriginalIndex.get(entity.data['start'] as number)
            const segmentTail = notesByOriginalIndex.get(entity.data['end'] as number)

            if (!head || !tail || !segmentHead || !segmentTail) continue

            const connectorIntermediate = createIntermediate('Connector', {
                head,
                tail,
                segmentHead,
                segmentTail,
                activeHead: segmentHead,
                activeTail: segmentTail,
            })

            head.data['connectorEase'] = easeTypeMapping[(entity.data['ease'] as number) ?? 0]
            head.data['segmentKind'] = connectorKind
            tail.data['segmentKind'] = connectorKind
            segmentHead.data['segmentKind'] = connectorKind

            connectorsByOriginalIndex.set(i, connectorIntermediate)
        }
    }

    for (const [i, note] of notesByOriginalIndex.entries()) {
        const entity = data.entities[i]

        const timescaleGroupIndex = (entity.data['timeScaleGroup'] as number) ?? -1
        if (timescaleGroupIndex >= 0 && timescaleGroupsByIndex.has(timescaleGroupIndex)) {
            note.data['#TIMESCALE_GROUP'] = timescaleGroupsByIndex.get(timescaleGroupIndex)!
        }

        const attachIndex = (entity.data['attach'] as number) ?? -1
        if (attachIndex > 0) {
            const attachConnector = connectorsByOriginalIndex.get(attachIndex)
            if (attachConnector) {
                note.data['attachHead'] = attachConnector.data['head']
                note.data['attachTail'] = attachConnector.data['tail']
                note.data['isAttached'] = 1
            }
        }

        const slideIndex = (entity.data['slide'] as number) ?? -1
        if (slideIndex > 0) {
            const slideConnector = connectorsByOriginalIndex.get(slideIndex)
            if (slideConnector) {
                note.data['activeHead'] = slideConnector.data['activeHead']
            }
        }
    }

    for (let i = 0; i < data.entities.length; i++) {
        const entity = data.entities[i]
        if (entity.archetype === 'SimLine') {
            const left = notesByOriginalIndex.get(entity.data['a'] as number)
            const right = notesByOriginalIndex.get(entity.data['b'] as number)
            if (left && right) {
                createIntermediate('SimLine', { left, right })
            }
        }
    }

    const anchorsByBeat = new Map<number, IntermediateEntity[]>()
    const anchorPositions = new Map<IntermediateEntity, Set<string>>()

    const getAnchor = (
        beat: number,
        lane: number,
        size: number,
        timescaleGroup: IntermediateEntity | undefined,
        pos: 'segmentHead' | 'segmentTail' | 'head' | 'tail',
        segmentKind: number = -1,
        segmentAlpha: number = -1,
        connectorEase: number = -1,
    ) => {
        let anchors = anchorsByBeat.get(beat)
        if (anchors) {
            for (const anchor of anchors) {
                if (anchorPositions.get(anchor)?.has(pos)) continue

                if (
                    anchor.data['lane'] === lane &&
                    anchor.data['size'] === size &&
                    anchor.data['#TIMESCALE_GROUP'] === timescaleGroup &&
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
                    if (segmentKind !== -1 && anchor.data['segmentKind'] === -1) {
                        anchor.data['segmentKind'] = segmentKind
                    }
                    if (segmentAlpha !== -1 && anchor.data['segmentAlpha'] === -1) {
                        anchor.data['segmentAlpha'] = segmentAlpha
                    }
                    if (connectorEase !== -1 && anchor.data['connectorEase'] === -1) {
                        anchor.data['connectorEase'] = connectorEase
                    }
                    anchorPositions.get(anchor)!.add(pos)
                    return anchor
                }
            }
        }

        const anchor = createIntermediate('AnchorNote', {
            '#BEAT': beat,
            lane,
            size,
            '#TIMESCALE_GROUP': timescaleGroup!,
            segmentKind,
            segmentAlpha,
            connectorEase,
        })

        if (!anchorsByBeat.has(beat)) {
            anchorsByBeat.set(beat, [])
        }
        anchorsByBeat.get(beat)!.push(anchor)

        anchorPositions.set(anchor, new Set([pos]))
        return anchor
    }

    for (let i = 0; i < data.entities.length; i++) {
        const entity = data.entities[i]
        if (entity.archetype === 'Guide') {
            const startBeat = entity.data['startBeat'] as number
            const startLane = entity.data['startLane'] as number
            const startSize = entity.data['startSize'] as number
            const startTimeScaleGroup = timescaleGroupsByIndex.get(
                entity.data['startTimeScaleGroup'] as number,
            )

            const headBeat = entity.data['headBeat'] as number
            const headLane = entity.data['headLane'] as number
            const headSize = entity.data['headSize'] as number
            const headTimeScaleGroup = timescaleGroupsByIndex.get(
                entity.data['headTimeScaleGroup'] as number,
            )

            const tailBeat = entity.data['tailBeat'] as number
            const tailLane = entity.data['tailLane'] as number
            const tailSize = entity.data['tailSize'] as number
            const tailTimeScaleGroup = timescaleGroupsByIndex.get(
                entity.data['tailTimeScaleGroup'] as number,
            )

            const endBeat = entity.data['endBeat'] as number
            const endLane = entity.data['endLane'] as number
            const endSize = entity.data['endSize'] as number
            const endTimeScaleGroup = timescaleGroupsByIndex.get(
                entity.data['endTimeScaleGroup'] as number,
            )

            const ease = easeTypeMapping[(entity.data['ease'] as number) ?? 0]
            const fade = (entity.data['fade'] as number) ?? 1
            const [startAlpha, endAlpha] = fadeAlphaMapping[fade]
            const kind = guideKindMapping[(entity.data['color'] as number) ?? 0]

            const start = getAnchor(
                startBeat,
                startLane,
                startSize,
                startTimeScaleGroup,
                'segmentHead',
                kind,
                startAlpha,
            )
            const end = getAnchor(
                endBeat,
                endLane,
                endSize,
                endTimeScaleGroup,
                'segmentTail',
                kind,
                endAlpha,
            )
            const head = getAnchor(
                headBeat,
                headLane,
                headSize,
                headTimeScaleGroup,
                'head',
                kind,
                -1,
                ease,
            )
            const tail = getAnchor(tailBeat, tailLane, tailSize, tailTimeScaleGroup, 'tail', kind)

            createIntermediate('Connector', {
                head,
                tail,
                segmentHead: start,
                segmentTail: end,
            })
        }
    }

    for (const anchorList of anchorsByBeat.values()) {
        for (const anchor of anchorList) {
            if (anchor.data['segmentKind'] === -1) {
                anchor.data['segmentKind'] = ConnectorKind.GUIDE_NEUTRAL
            }
            if (anchor.data['segmentAlpha'] === -1) {
                anchor.data['segmentAlpha'] = 1.0
            }
            if (anchor.data['connectorEase'] === -1) {
                anchor.data['connectorEase'] = EaseType.LINEAR
            }
        }
    }

    for (const entity of allIntermediateEntities) {
        if (entity.archetype === 'Connector') {
            const head = entity.data['head'] as IntermediateEntity
            const tail = entity.data['tail'] as IntermediateEntity
            if (head && tail) {
                head.data['next'] = tail
            }
        }
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

    const getRef = (intermediateEntity: IntermediateEntity): string => {
        let ref = intermediateToRef.get(intermediateEntity)
        if (ref) return ref
        ref = (entityRefCounter++).toString(16)
        intermediateToRef.set(intermediateEntity, ref)
        return ref
    }

    for (const intermediateEntity of allIntermediateEntities) {
        const entity: LevelDataEntity = {
            archetype: intermediateEntity.archetype,
            name: getRef(intermediateEntity),
            data: [],
        }

        for (const [dataName, dataValue] of Object.entries(intermediateEntity.data)) {
            if (typeof dataValue === 'number') {
                entity.data.push({ name: dataName, value: dataValue })
            } else if (dataValue !== undefined && dataValue !== null) {
                entity.data.push({ name: dataName, ref: getRef(dataValue as IntermediateEntity) })
            }
        }

        entities.push(entity)
    }

    return {
        bgmOffset: data.bgmOffset + offset,
        entities,
    }
}
