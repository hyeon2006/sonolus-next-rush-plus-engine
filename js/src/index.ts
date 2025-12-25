import { DatabaseEngineItem, LevelData } from '@sonolus/core'
import { mmwsToUSC } from './mmw/convert.js'
import { susToUSC } from './sus/convert.js'
import { uscToLevelData } from './usc/convert.js'
import { USC } from './usc/index.js'

export { susToUSC, mmwsToUSC, uscToLevelData }
export * from './usc/index.js'

export const convertToLevelData = (
    input: string | Uint8Array | USC | LevelData,
    offset = 0,
): LevelData => {
    if (isLevelData(input)) {
        return input
    }

    let usc: USC

    if (isUSC(input)) {
        usc = input
    } else if (input instanceof Uint8Array) {
        usc = mmwsToUSC(input)
    } else if (typeof input === 'string') {
        try {
            const parsed = JSON.parse(input)
            if (isLevelData(parsed)) {
                return parsed
            }
            if (isUSC(parsed)) {
                usc = parsed
            } else {
                usc = susToUSC(input)
            }
        } catch {
            usc = susToUSC(input)
        }
    } else {
        throw new Error(
            'Unsupported input type: Input must be string(SUS/USC/LevelData), Uint8Array(MMWS), or USC/LevelData object.',
        )
    }

    return uscToLevelData(usc, offset)
}

function isUSC(data: unknown): data is USC {
    return (
        typeof data === 'object' &&
        data !== null &&
        'objects' in data &&
        Array.isArray((data as any).objects)
    )
}

function isLevelData(data: unknown): data is LevelData {
    return (
        typeof data === 'object' &&
        data !== null &&
        'entities' in data &&
        Array.isArray((data as any).entities)
    )
}

export const version = '0.0.0'

export const databaseEngineItem = {
    name: 'next-rush-plus',
    version: 13,
    title: {
        en: 'Next RUSH+',
    },
    subtitle: {
        en: 'Next RUSH+',
    },
    author: {
        en: 'Next RUSH+',
    },
    description: {
        en: [
            "Next SEKAI's expansion engine",
            `Version: ${version}`,
            '',
            'https://github.com/Next-SEKAI/sonolus-next-sekai-engine',
        ].join('\n'),
        ko: [
            'Next SEKAI의 확장 엔진',
            `버전: ${version}`,
            '',
            'https://github.com/Next-SEKAI/sonolus-next-sekai-engine',
        ].join('\n'),
    },
} as const satisfies Partial<DatabaseEngineItem>
