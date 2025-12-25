import BinarySeeker from '@sevenc-nanashi/binaryseeker'

const FlickType = ['none', 'up', 'left', 'right'] as const
type FlickType = (typeof FlickType)[number]
const StepType = ['visible', 'hidden', 'ignored'] as const
type StepType = (typeof StepType)[number]
const EaseType = ['linear', 'easeIn', 'easeOut', 'easeInOut', 'easeOutIn'] as const
export type EaseType = (typeof EaseType)[number]

export type Score = {
    metadata: {
        title: string
        author: string
        artist: string
        musicFile: string
        musicOffset: number
        jacketFile: string
    }
    events: {
        timeSignatures: {
            measure: number
            numerator: number
            denominator: number
        }[]
        bpmChanges: {
            tick: number
            bpm: number
        }[]
        hispeedChanges: {
            tick: number
            speed: number
            layer: number
        }[]
        skills: number[]
        fever: {
            start: number
            end: number
        }
    }
    taps: {
        tick: number
        lane: number
        width: number
        flickType: FlickType
        flags: {
            critical: boolean
            friction: boolean
        }
        layer: number
    }[]
    holds: {
        flags: {
            startHidden: boolean
            endHidden: boolean
            guide: boolean
        }
        start: {
            tick: number
            lane: number
            width: number
            flags: {
                critical: boolean
                friction: boolean
            }
            layer: number
            ease: EaseType
        }
        fadeType: number
        guideColor: number
        steps: {
            tick: number
            lane: number
            width: number
            type: StepType
            ease: EaseType
            layer: number
        }[]
        end: {
            tick: number
            lane: number
            width: number
            flickType: FlickType

            flags: {
                critical: boolean
                friction: boolean
            }

            layer: number
        }
    }[]
    damages: {
        tick: number
        lane: number
        width: number
        flickType: FlickType
        flags: {
            critical: boolean
            friction: boolean
        }

        layer: number
    }[]
    numLayers: number
}

export const analyze = (mmws: Uint8Array): Score => {
    const buffer = new BinarySeeker(mmws.buffer)
    const header = buffer.readString()
    if (header !== 'MMWS' && header !== 'CCMMWS') {
        throw new Error('Invalid MMWS file')
    }
    const version = buffer.readInt16LE()
    let cyanvasVersion = buffer.readInt16LE()
    if (version < 3) {
        throw new Error('Unsupported MMWS version')
    }
    if (header === 'CCMMWS' && cyanvasVersion === 0) {
        cyanvasVersion = 1
    }

    const metadataPointer = buffer.readUInt32LE()
    const eventsPointer = buffer.readUInt32LE()
    const tapsPointer = buffer.readUInt32LE()
    const holdsPointer = buffer.readUInt32LE()
    const damagesPointer = cyanvasVersion > 0 ? buffer.readUInt32LE() : 0
    const layersPointer = cyanvasVersion >= 4 ? buffer.readUInt32LE() : 0
    // const waypointsPointer = cyanvasVersion >= 5 ? buffer.readUInt32LE() : 0

    buffer.seek(metadataPointer)
    const metadata = {
        title: buffer.readString(),
        author: buffer.readString(),
        artist: buffer.readString(),
        musicFile: buffer.readString(),
        musicOffset: buffer.readFloat32LE(),
        jacketFile: buffer.readString(),
    }

    buffer.seek(eventsPointer)
    const events: Score['events'] = {
        timeSignatures: [],
        bpmChanges: [],
        hispeedChanges: [],
        skills: [],
        fever: {
            start: 0,
            end: 0,
        },
    }
    const timeSignaturesCount = buffer.readInt32LE()
    for (let i = 0; i < timeSignaturesCount; i++) {
        events.timeSignatures.push({
            measure: buffer.readInt32LE(),
            numerator: buffer.readInt32LE(),
            denominator: buffer.readInt32LE(),
        })
    }
    const bpmChangesCount = buffer.readInt32LE()
    for (let i = 0; i < bpmChangesCount; i++) {
        events.bpmChanges.push({
            tick: buffer.readInt32LE(),
            bpm: buffer.readFloat32LE(),
        })
    }
    const hispeedChangesCount = buffer.readInt32LE()
    for (let i = 0; i < hispeedChangesCount; i++) {
        events.hispeedChanges.push({
            tick: buffer.readInt32LE(),
            speed: buffer.readFloat32LE(),
            layer: cyanvasVersion >= 4 ? buffer.readInt32LE() : 0,
        })
    }
    const skillsCount = buffer.readInt32LE()
    for (let i = 0; i < skillsCount; i++) {
        events.skills.push(buffer.readInt32LE())
    }
    events.fever.start = buffer.readInt32LE()
    events.fever.end = buffer.readInt32LE()

    buffer.seek(tapsPointer)

    const taps: Score['taps'] = []
    const tapsCount = buffer.readInt32LE()
    for (let i = 0; i < tapsCount; i++) {
        const tick = buffer.readInt32LE()

        const lane = buffer.readInt32LE()
        const width = buffer.readInt32LE()
        const layer = cyanvasVersion >= 4 ? buffer.readInt32LE() : 0

        const flickType = FlickType[buffer.readInt32LE() as 0 | 1 | 2 | 3]
        const flags = buffer.readInt32LE()
        taps.push({
            tick,

            lane,
            width,
            flickType,
            flags: {
                critical: !!(flags & (1 << 0)),
                friction: !!(flags & (1 << 1)),
            },
            layer,
        })
    }

    buffer.seek(holdsPointer)
    const holds: Score['holds'] = []
    const holdsCount = buffer.readInt32LE()
    for (let i = 0; i < holdsCount; i++) {
        const holdFlags = version >= 4 ? buffer.readInt32LE() : 0
        const startTick = buffer.readInt32LE()
        const startLane = buffer.readInt32LE()
        const startWidth = buffer.readInt32LE()
        const startLayer = cyanvasVersion >= 4 ? buffer.readInt32LE() : 0
        const startFlags = buffer.readInt32LE()
        const startEase = EaseType[buffer.readInt32LE() as 0 | 1 | 2]
        const fadeType = cyanvasVersion >= 2 ? buffer.readInt32LE() : 0
        const guideColor =
            cyanvasVersion >= 3 ? buffer.readInt32LE() : startFlags & (1 << 0) ? 4 : 2
        const stepsCount = buffer.readInt32LE()
        const steps: Score['holds'][0]['steps'] = []
        for (let j = 0; j < stepsCount; j++) {
            const tick = buffer.readInt32LE()
            const lane = buffer.readInt32LE()
            const width = buffer.readInt32LE()
            const layer = cyanvasVersion >= 4 ? buffer.readInt32LE() : 0
            buffer.readInt32LE() // unused flags
            const type = StepType[buffer.readInt32LE()]
            const ease = EaseType[buffer.readInt32LE()]
            steps.push({
                tick,
                lane,
                width,
                type,
                ease,

                layer,
            })
        }
        const endTick = buffer.readInt32LE()
        const endLane = buffer.readInt32LE()
        const endWidth = buffer.readInt32LE()
        const endLayer = cyanvasVersion >= 4 ? buffer.readInt32LE() : 0
        const endFlickType = FlickType[buffer.readInt32LE() as 0 | 1 | 2 | 3]
        const endFlags = buffer.readInt32LE()

        holds.push({
            flags: {
                startHidden: !!(holdFlags & (1 << 0)),
                endHidden: !!(holdFlags & (1 << 1)),
                guide: !!(holdFlags & (1 << 2)),
            },
            start: {
                tick: startTick,
                lane: startLane,
                width: startWidth,
                ease: startEase,
                flags: {
                    critical: !!(startFlags & (1 << 0)),
                    friction: !!(startFlags & (1 << 1)),
                },
                layer: startLayer,
            },
            fadeType,
            guideColor,
            steps,
            end: {
                tick: endTick,
                lane: endLane,
                width: endWidth,
                flags: {
                    critical: !!(endFlags & (1 << 0)),
                    friction: !!(endFlags & (1 << 1)),
                },
                flickType: endFlickType,
                layer: endLayer,
            },
        })
    }

    events.timeSignatures.sort((a, b) => a.measure - b.measure)
    events.bpmChanges.sort((a, b) => a.tick - b.tick)
    events.hispeedChanges.sort((a, b) => a.tick - b.tick)
    events.skills.sort((a, b) => a - b)
    taps.sort((a, b) => a.tick - b.tick)
    holds.sort((a, b) => a.start.tick - b.start.tick)

    const damages: Score['damages'] = []
    if (cyanvasVersion >= 1) {
        buffer.seek(damagesPointer)
        const damagesCount = buffer.readInt32LE()
        for (let i = 0; i < damagesCount; i++) {
            const tick = buffer.readInt32LE()

            const lane = buffer.readInt32LE()
            const width = buffer.readInt32LE()

            const layer = cyanvasVersion >= 4 ? buffer.readInt32LE() : 0

            const flickType = FlickType[buffer.readInt32LE() as 0 | 1 | 2 | 3]
            const flags = buffer.readInt32LE()
            damages.push({
                tick,

                lane,
                width,
                flickType,
                layer,
                flags: {
                    critical: !!(flags & (1 << 0)),
                    friction: !!(flags & (1 << 1)),
                },
            })
        }
        damages.sort((a, b) => a.tick - b.tick)
    }

    let numLayers = 1
    if (cyanvasVersion >= 4) {
        buffer.seek(layersPointer)
        numLayers = buffer.readInt32LE()
    }

    return {
        metadata,
        events,
        taps,
        holds,
        damages,
        numLayers,
    }
}
