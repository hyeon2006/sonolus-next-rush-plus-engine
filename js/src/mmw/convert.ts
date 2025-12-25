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
        if (tap.flickType !== 'none') {
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
        if (hold.end.flickType !== 'none') {
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
