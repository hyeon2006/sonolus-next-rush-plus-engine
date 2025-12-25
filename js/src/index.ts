import { DatabaseEngineItem } from '@sonolus/core'

export { susToUSC } from './sus/convert.js'
export { mmwsToUSC } from './mmw/convert.js'
export { uscToLevelData } from './usc/convert.js'
export * from './usc/index.js'

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
