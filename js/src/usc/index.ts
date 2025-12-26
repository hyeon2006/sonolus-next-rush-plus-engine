export type USC = {
    offset: number
    objects: USCObject[]
}

export type USCObject =
    | USCBpmChange
    | USCTimeScaleChange
    | USCSingleNote
    | USCSlideNote
    | USCGuideNote
    | USCDamageNote
    | USCEvent

type BaseUSCObject = {
    beat: number
    timeScaleGroup: number
}

export type USCBpmChange = Omit<BaseUSCObject, 'timeScaleGroup'> & {
    type: 'bpm'
    bpm: number
}

export type USCTimeScaleChange = {
    type: 'timeScaleGroup'
    changes: {
        beat: number
        timeScale: number
    }[]
}

type BaseUSCNote = BaseUSCObject & {
    lane: number
    size: number
}

export type USCSingleNote = BaseUSCNote & {
    type: 'single'
    critical: boolean
    trace: boolean
    direction?: 'left' | 'up' | 'right' | 'none'
}

export type USCDamageNote = BaseUSCNote & {
    type: 'damage'
}

export type USCConnectionStartNote = BaseUSCNote & {
    type: 'start'
    critical: boolean
    ease: 'out' | 'linear' | 'in' | 'inout' | 'outin'
    judgeType: 'normal' | 'trace' | 'none'
}

export type USCConnectionTickNote = BaseUSCNote & {
    type: 'tick'
    critical?: boolean
    ease: 'out' | 'linear' | 'in' | 'inout' | 'outin'
    judgeType?: 'normal' | 'trace'
}

export type USCConnectionAttachNote = Omit<BaseUSCObject, 'timeScaleGroup'> & {
    type: 'attach'
    critical?: boolean
    timeScaleGroup?: number
}

export type USCConnectionEndNote = BaseUSCNote & {
    type: 'end'
    critical: boolean
    direction?: 'left' | 'up' | 'right'
    judgeType: 'normal' | 'trace' | 'none'
}

export type USCSlideNote = {
    type: 'slide' | 'guide'
    critical: boolean
    connections: [
        USCConnectionStartNote,
        ...(USCConnectionTickNote | USCConnectionAttachNote)[],
        USCConnectionEndNote,
    ]
}
export const USCColor = {
    neutral: 0,
    red: 1,
    green: 2,
    blue: 3,
    yellow: 4,
    purple: 5,
    cyan: 6,
    black: 7,
}
export type USCColor = keyof typeof USCColor

export type USCGuideMidpointNote = BaseUSCNote & {
    ease: 'out' | 'linear' | 'in' | 'inout' | 'outin'
}

export const USCFade = {
    in: 2,
    out: 0,
    none: 1,
}
export type USCFade = keyof typeof USCFade
export type USCGuideNote = {
    type: 'guide'
    color: USCColor
    fade: USCFade
    midpoints: USCGuideMidpointNote[]
}
export const SkillTypes = {
    heal: 0,
    score: 1,
    judgment: 2,
} as const
export type USCEvent = {
    type: 'skill' | 'feverChance' | 'feverStart'
    force?: boolean
    types?: number
    level?: number
    beat: number
}
