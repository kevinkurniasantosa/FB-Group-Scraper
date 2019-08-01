//
// Freelance job contact me: joseph0x01@gmail.com
//
// Hardcoding common districts mapping for accuracy and performance
//
// https://en.wikipedia.org/wiki/Districts_of_Hong_Kong
const addresses = [
  {
    keys: ['中西区', '中西區', 'CENTRAL', 'CENTRAL AND WESTERN DISTRICT'],
    value: [
      {
        lat: '22.2793278',
        lon: '114.1628131',
        name: 'CENTRAL AND WESTERN DISTRICT'
      }
    ]
  },
  {
    keys: ['东区', '東區', 'EASTERN DISTRICT'],
    value: [
      {
        lat: '22.28411',
        lon: '114.22',
        name: 'EASTERN DISTRICT'
      }
    ]
  },
  {
    keys: ['南区', '南區', 'SOUTHERN DISTRICT'],
    value: [
      {
        lat: '22.24725',
        lon: '114.15884',
        name: 'SOUTHERN DISTRICT'
      }
    ]
  },
  {
    keys: ['湾仔区', '灣仔區', 'WANCHAI', 'WAN CHAI DISTRICT'],
    value: [
      {
        lat: '22.27968',
        lon: '114.17168',
        name: 'WAN CHAI DISTRICT'
      }
    ]
  },
  {
    keys: ['深水埗区', '深水埗區', 'SHAM SHUI PO DISTRICT'],
    value: [
      {
        lat: '22.33074',
        lon: '114.1622',
        name: 'SHAM SHUI PO DISTRICT'
      }
    ]
  },
  {
    keys: ['九龙城区', '九龍城區', 'KOWLOON CITY'],
    value: [
      {
        lat: '22.3282',
        lon: '114.19155',
        name: 'KOWLOON CITY'
      }
    ]
  },
  {
    keys: ['观塘区', '觀塘區', 'KWUNG TONG', 'KWUN TONG DISTRICT'],
    value: [
      {
        lat: '22.31326',
        lon: '114.22581',
        name: 'KWUN TONG DISTRICT'
      }
    ]
  },
  {
    keys: ['黄大仙区', '黃大仙區', 'WONG TAI SIN', 'WONG TAI SIN DISTRICT'],
    value: [
      {
        lat: '22.33353',
        lon: '114.19686',
        name: 'WONG TAI SIN DISTRICT'
      }
    ]
  },
  {
    keys: ['油尖旺区', '油尖旺區', 'YAU TSIM MONG', 'MONGKOK', 'MONG KOK', 'MK', 'TST', 'TSIM SHA TSUI', 'YAU TSIM MONG DISTRICT'],
    value: [
      {
        lat: '22.32138',
        lon: '114.1726',
        name: 'YAU TSIM MONG DISTRICT'
      }
    ]
  },
  {
    keys: ['離島區', 'ISLANDS DISTRICT'],
    value: [
      {
        lat: '22.26114',
        lon: '113.94608',
        name: 'ISLANDS DISTRICT'
      }
    ]
  },
  {
    keys: ['离岛区', '葵青區', 'KWAI TSING', 'KWAI TSING DISTRICT'],
    value: [
      {
        lat: '22.35488',
        lon: '114.08401',
        name: 'KWAI TSING DISTRICT'
      }
    ]
  },
  {
    keys: ['北区', '北區', 'NORTH DISTRICT'],
    value: [
      {
        lat: '22.49471',
        lon: '114.13812',
        name: 'NORTH DISTRICT'
      }
    ]
  },
  {
    keys: ['西贡区', '西貢區', 'SAI KUNG', 'SAI KUNG DISTRICT'],
    value: [
      {
        lat: '22.38143',
        lon: '114.27052',
        name: 'SAI KUNG DISTRICT'
      }
    ]
  },
  {
    keys: ['沙田区', '沙田區', 'SHA TIN', 'SHATIN', 'SHA TIN DISTRICT'],
    value: [
      {
        lat: '22.38715',
        lon: '114.19534',
        name: 'SHA TIN DISTRICT'
      }
    ]
  },
  {
    keys: ['大埔区', '大埔區', 'TAI PO', 'TAIPO', 'TAI PO DISTRICT'],
    value: [
      {
        lat: '22.45085',
        lon: '114.16422',
        name: 'TAI PO DISTRICT'
      }
    ]
  },
  {
    keys: ['荃湾区', '荃灣區', 'TSUEN WAN', 'TSUEN WAN DISTRICT'],
    value: [
      {
        lat: '22.36281',
        lon: '114.12907',
        name: 'TSUEN WAN DISTRICT'
      }
    ]
  },
  {
    keys: ['屯门区', '屯門區', 'TUEN MUN', 'TUEN MUN DISTRICT'],
    value: [
      {
        lat: '22.39211',
        lon: '113.97011',
        name: 'TUEN MUN DISTRICT'
      }
    ]
  },
  {
    keys: ['元朗区', '元朗區', 'YUEN LONG', 'YUEN LONG DISTRICT'],
    value: [
      {
        lat: '22.44559',
        lon: '114.02218',
        name: 'YUEN LONG DISTRICT'
      }
    ]
  },
  {
    keys: ['西环', '西環', 'SAI WAN', 'WESTERN DISTRICT', 'WESTERN'],
    value: [
      {
        lat: '22.285',
        lon: '114.132',
        name: 'WESTERN DISTRICT'
      }
    ]
  }
]

module.exports = { addresses }

