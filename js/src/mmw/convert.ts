import {
    USC,
    USCColor,
    USCConnectionAttachNote,
    USCConnectionEndNote,
    USCConnectionStartNote,
    USCConnectionTickNote,
    USCDamageNote,
    USCGuideNote,
    USCSingleNote,
    USCSlideNote,
} from '../usc/index.js'
import { EaseType, analyze } from './analyze.js'
import { type LevelData } from '@sonolus/core'

const mmwsEaseToUSCEase = {
    linear: 'linear',
    easeOut: 'out',
    easeIn: 'in',
    easeInOut: 'inout',
    easeOutIn: 'outin',
} as const satisfies Record<EaseType, string>
const ticksPerBeat = 480
const laneToUSCLane = ({ lane, width }: { lane: number; width: number }): number => {
    return lane - 6 + width / 2
}

/**
 * Convert MMWS or CCMMWS to a USC
 */
export const mmwsToUSC = (mmws: Uint8Array): USC => {
    const score = analyze(mmws)
    const usc: USC = {
        objects: [],
        offset: score.metadata.musicOffset / -1000,
    }

    for (const bpmChange of score.events.bpmChanges) {
        usc.objects.push({
            type: 'bpm',
            beat: bpmChange.tick / ticksPerBeat,
            bpm: bpmChange.bpm,
        })
    }
    const tsGroups = new Map<number, { beat: number; timeScale: number }[]>()
    for (let i = 0; i < score.numLayers; i++) {
        tsGroups.set(i, [])
    }
    for (const hispeedChange of score.events.hispeedChanges) {
        const key = hispeedChange.layer
        if (!tsGroups.has(key)) {
            throw new Error('Invalid layer')
        }
        tsGroups.get(key)!.push({
            beat: hispeedChange.tick / ticksPerBeat,
            timeScale: hispeedChange.speed,
        })
    }
    for (const changes of tsGroups.values()) {
        usc.objects.push({
            type: 'timeScaleGroup',
            changes,
        })
    }

    for (const tap of score.taps) {
        const uscTap: USCSingleNote = {
            type: 'single',
            beat: tap.tick / ticksPerBeat,
            timeScaleGroup: tap.layer,
            critical: tap.flags.critical,
            lane: laneToUSCLane(tap),
            size: tap.width / 2,
            trace: tap.flags.friction,
        }
        if (tap.flickType === 'up' || tap.flickType === 'left' || tap.flickType === 'right') {
            uscTap.direction = tap.flickType
        }
        usc.objects.push(uscTap)
    }
    for (const hold of score.holds) {
        const uscStartNote: USCConnectionStartNote = {
            type: 'start',
            beat: hold.start.tick / ticksPerBeat,
            timeScaleGroup: hold.start.layer,
            critical: hold.start.flags.critical,
            ease: mmwsEaseToUSCEase[hold.start.ease],
            lane: laneToUSCLane(hold.start),
            size: hold.start.width / 2,
            judgeType: hold.flags.startHidden
                ? 'none'
                : hold.start.flags.friction
                  ? 'trace'
                  : 'normal',
        }
        const uscEndNote: USCConnectionEndNote = {
            type: 'end',
            beat: hold.end.tick / ticksPerBeat,
            timeScaleGroup: hold.end.layer,
            critical: hold.end.flags.critical,
            lane: laneToUSCLane(hold.end),
            size: hold.end.width / 2,
            judgeType: hold.flags.endHidden ? 'none' : hold.end.flags.friction ? 'trace' : 'normal',
        }
        if (
            hold.end.flickType === 'up' ||
            hold.end.flickType === 'left' ||
            hold.end.flickType === 'right'
        ) {
            uscEndNote.direction = hold.end.flickType
        }

        if (hold.flags.guide) {
            const uscGuide: USCGuideNote = {
                type: 'guide',
                fade: hold.fadeType === 0 ? 'out' : hold.fadeType === 1 ? 'none' : 'in',
                color: Object.entries(USCColor).find(
                    ([, i]) => i === hold.guideColor,
                )![0] as USCColor,
                midpoints: [hold.start, ...hold.steps, hold.end].map((step) => ({
                    beat: step.tick / ticksPerBeat,
                    lane: laneToUSCLane(step),
                    size: step.width / 2,
                    timeScaleGroup: step.layer,
                    ease: 'ease' in step ? mmwsEaseToUSCEase[step.ease] : 'linear',
                })),
            }
            usc.objects.push(uscGuide)
        } else {
            const uscSlide: USCSlideNote = {
                type: 'slide',
                critical: hold.start.flags.critical,
                connections: [
                    uscStartNote,
                    ...hold.steps.map((step) => {
                        const beat = step.tick / ticksPerBeat
                        const lane = laneToUSCLane(step)
                        const size = step.width / 2
                        if (step.type === 'ignored') {
                            return {
                                type: 'attach',
                                beat,
                                critical: hold.start.flags.critical,
                                timeScaleGroup: step.layer,
                            } satisfies USCConnectionAttachNote
                        } else {
                            const uscStep: USCConnectionTickNote = {
                                type: 'tick',
                                beat,

                                timeScaleGroup: step.layer,
                                lane,
                                size,
                                ease: mmwsEaseToUSCEase[step.ease],
                            }
                            if (step.type === 'visible') {
                                uscStep.critical = hold.start.flags.critical
                            }

                            return uscStep
                        }
                    }),
                    uscEndNote,
                ],
            }
            usc.objects.push(uscSlide)
        }
    }

    for (const damage of score.damages) {
        const uscDamage: USCDamageNote = {
            type: 'damage',
            beat: damage.tick / ticksPerBeat,
            timeScaleGroup: damage.layer,
            lane: laneToUSCLane(damage),
            size: damage.width / 2,
        }
        usc.objects.push(uscDamage)
    }

    return usc
}

/**
 * Convert CCMMWS to a USC
 */
export const ccmmwsToUSC = mmwsToUSC

const laneToSonolusLane = ({ lane, width }: { lane: number; width: number }): number => {
    return lane - 6 + width / 2
}

const flickTypeToDirection = (type: string): number => {
    switch (type) {
        case 'up':
            return 0
        case 'left':
            return 1
        case 'right':
            return 2
        case 'down':
            return 3
        case 'down_left':
            return 4
        case 'down_right':
            return 5
        default:
            return 0
    }
}

const resolveArchetype = (baseName: string, isDummy: boolean): string => {
    return isDummy ? `Fake${baseName}` : baseName
}

const resolveConnectorKind = (isCritical: boolean, isDummy: boolean): number => {
    if (isDummy) {
        return isCritical ? 52 : 51
    }
    return isCritical ? 1 : 0
}

/**
 * Convert UCMMWS to a LevelData
 */
export const ucmmwsToLevelData = (mmws: Uint8Array): LevelData => {
    const score = analyze(mmws)

    const entities: LevelData['entities'] = []
    const ticksPerBeat = 480

    entities.push({
        archetype: 'Initialization',
        data: [],
    })

    entities.push({
        archetype: 'Stage',
        data: [],
    })

    for (const bpm of score.events.bpmChanges) {
        entities.push({
            archetype: 'BPMChange',
            data: [
                { name: 'beat', value: bpm.tick / ticksPerBeat },
                { name: 'bpm', value: bpm.bpm },
            ],
        })
    }

    for (const hs of score.events.hispeedChanges) {
        const data = [
            { name: 'beat', value: hs.tick / ticksPerBeat },
            { name: 'timeScale', value: hs.speed },
        ]

        if (hs.skip !== undefined && hs.skip !== 0) {
            data.push({ name: '#TIMESCALE_SKIP', value: hs.skip })
        }
        if (hs.ease !== undefined) {
            data.push({ name: '#TIMESCALE_EASE', value: hs.ease })
        }
        if (hs.hideNotes !== undefined) {
            data.push({ name: 'hideNotes', value: hs.hideNotes ? 1 : 0 })
        }

        entities.push({
            archetype: 'TimeScaleChange',
            data: data,
        })
    }

    for (const tap of score.taps) {
        const isDummy = !!tap.flags.dummy
        const isCritical = tap.flags.critical
        const isFlick = tap.flickType !== 'none'

        let baseArchetype = ''
        if (isFlick) {
            baseArchetype = isCritical ? 'CriticalFlickNote' : 'NormalFlickNote'
        } else {
            baseArchetype = isCritical ? 'CriticalTapNote' : 'NormalTapNote'
        }

        const archetype = resolveArchetype(baseArchetype, isDummy)

        const data = [
            { name: 'beat', value: tap.tick / ticksPerBeat },
            { name: 'lane', value: laneToSonolusLane(tap) },
            { name: 'size', value: tap.width },
            { name: 'timeScaleGroup', value: tap.layer },
        ]

        if (isFlick) {
            data.push({ name: 'direction', value: flickTypeToDirection(tap.flickType) })
        }

        entities.push({
            archetype,
            data,
        })
    }

    for (const hold of score.holds) {
        const isDummy = !!hold.flags.dummy
        const isCritical = hold.start.flags.critical

        const headBase = isCritical ? 'CriticalHeadTapNote' : 'NormalHeadTapNote'
        const headArchetype = resolveArchetype(headBase, isDummy)

        const headIndex = entities.length
        entities.push({
            archetype: headArchetype,
            data: [
                { name: 'beat', value: hold.start.tick / ticksPerBeat },
                { name: 'lane', value: laneToSonolusLane(hold.start) },
                { name: 'size', value: hold.start.width },
                { name: 'timeScaleGroup', value: hold.start.layer },
            ],
        })

        let prevIndex = headIndex

        for (const step of hold.steps) {
            if (step.type === 'visible') {
                const tickBase = isCritical ? 'CriticalTickNote' : 'NormalTickNote'
                const tickArchetype = resolveArchetype(tickBase, isDummy)

                const tickIndex = entities.length
                entities.push({
                    archetype: tickArchetype,
                    data: [
                        { name: 'beat', value: step.tick / ticksPerBeat },
                        { name: 'lane', value: laneToSonolusLane(step) },
                        { name: 'size', value: step.width },
                        { name: 'timeScaleGroup', value: step.layer },
                    ],
                })

                entities.push({
                    archetype: 'Connector',
                    data: [
                        { name: 'head', value: prevIndex },
                        { name: 'tail', value: tickIndex },
                        { name: 'kind', value: resolveConnectorKind(isCritical, isDummy) },
                    ],
                })
                prevIndex = tickIndex
            }
        }

        const isTailFlick = hold.end.flickType !== 'none'
        let tailBase = ''
        if (isTailFlick) {
            tailBase = isCritical ? 'CriticalTailFlickNote' : 'NormalTailFlickNote'
        } else {
            tailBase = isCritical ? 'CriticalTailTapNote' : 'NormalTailTapNote'
        }
        const tailArchetype = resolveArchetype(tailBase, isDummy)

        const tailIndex = entities.length
        const tailData = [
            { name: 'beat', value: hold.end.tick / ticksPerBeat },
            { name: 'lane', value: laneToSonolusLane(hold.end) },
            { name: 'size', value: hold.end.width },
            { name: 'timeScaleGroup', value: hold.end.layer },
        ]
        if (isTailFlick) {
            tailData.push({ name: 'direction', value: flickTypeToDirection(hold.end.flickType) })
        }

        entities.push({
            archetype: tailArchetype,
            data: tailData,
        })

        entities.push({
            archetype: 'Connector',
            data: [
                { name: 'head', value: prevIndex },
                { name: 'tail', value: tailIndex },
                { name: 'kind', value: resolveConnectorKind(isCritical, isDummy) },
            ],
        })
    }

    for (const damage of score.damages) {
        const isDummy = !!damage.flags.dummy
        const archetype = resolveArchetype('DamageNote', isDummy)

        entities.push({
            archetype,
            data: [
                { name: 'beat', value: damage.tick / ticksPerBeat },
                { name: 'lane', value: laneToSonolusLane(damage) },
                { name: 'size', value: damage.width },
                { name: 'timeScaleGroup', value: damage.layer },
            ],
        })
    }

    return {
        bgmOffset: score.metadata.musicOffset / 1000,
        entities,
    }
}
