import releaseManifest from './release.json'

const windowsDownloadUrl = import.meta.env.VITE_WINDOWS_DOWNLOAD_URL || releaseManifest.windows.downloadUrl

export const release = {
  ...releaseManifest,
  version: import.meta.env.VITE_GAME_VERSION || releaseManifest.version,
  windows: {
    ...releaseManifest.windows,
    downloadUrl: windowsDownloadUrl,
    fileSize: import.meta.env.VITE_WINDOWS_FILE_SIZE || releaseManifest.windows.fileSize,
    sha256: import.meta.env.VITE_WINDOWS_SHA256 || (import.meta.env.VITE_WINDOWS_DOWNLOAD_URL ? '' : releaseManifest.windows.sha256),
  },
}

export const gallery = [
  { src: '/images/gallery/cg_girl_first.jpg', title: 'The Girl in the Hallway', type: 'STORY CG' },
  { src: '/images/gallery/cg_confrontation.jpg', title: 'The Listener', type: 'CLIMAX' },
  { src: '/images/gallery/cg_hidden_room.jpg', title: 'The Hidden Room', type: 'STORY CG' },
  { src: '/images/gallery/cg_jumpscare.jpg', title: 'Don’t Open the Door', type: 'NIGHTMARE' },
  { src: '/images/gallery/cg_mirror.jpg', title: 'Let Me Out', type: 'STORY CG' },
  { src: '/images/gallery/cg_bargain_flashback.jpg', title: 'The Bargain', type: 'MEMORY' },
  { src: '/images/gallery/cg_parents.jpg', title: 'What We Did', type: 'MEMORY' },
  { src: '/images/gallery/cg_ending_truth.jpg', title: 'The Truth', type: 'ENDING' },
  { src: '/images/gallery/cg_ending_alone.jpg', title: 'You Were Never Alone', type: 'ENDING' },
  { src: '/images/gallery/cg_ending_call.jpg', title: 'The Seventh Call', type: 'ENDING' },
  { src: '/images/gallery/cg_ending_newgame.jpg', title: 'New Game', type: 'ENDING' },
  { src: '/images/gallery/cg_phone_photo.jpg', title: '3:00 AM', type: 'EVIDENCE' },
]

export const characters = [
  {
    name: 'Ethan', role: 'THE RETURNING TENANT', image: '/images/characters/ethan_neutral.png',
    description: 'Seven years away. One key that remembers the way home. Ethan is certain he has never lived in Apartment 3B before.',
    accent: 'amber',
  },
  {
    name: 'The Girl', role: 'THE VOICE IN THE WALLS', image: '/images/characters/girl_neutral.png',
    description: 'She knows the rooms behind the rooms. She knows what Ethan promised. She has been waiting for him to remember.',
    accent: 'ice',
  },
  {
    name: 'Maya', role: 'THE NEIGHBOR IN 3A', image: '/images/characters/maya_neutral.png',
    description: 'A warm cup of coffee. A warning about the phone. The only person on Ashgrove Street who still feels real.',
    accent: 'rose',
  },
  {
    name: 'The Entity', role: 'THE LISTENER', image: '/images/characters/entity_evil.png',
    description: 'It does not need to chase you. It only needs you to answer when it calls.',
    accent: 'blood',
  },
]

export const features = [
  { icon: 'eye', number: '01', title: 'Psychological horror', text: 'A slow descent built from familiar rooms, unreliable memories, and the sound coming from the other side of the wall.' },
  { icon: 'split', number: '02', title: 'Choices that stay', text: 'Decide who to trust, what to investigate, and which voice deserves an answer.' },
  { icon: 'heart', number: '03', title: 'A fragile sanity', text: 'Your sense of what is real shifts as the apartment reveals the memories you buried.' },
  { icon: 'search', number: '04', title: 'Investigate every room', text: 'Examine photographs, recordings, and traces left behind by the people who lived here before.' },
  { icon: 'zap', number: '05', title: 'Moments of terror', text: 'Unsettling reveals and carefully timed scares punctuate the quiet.' },
  { icon: 'layers', number: '06', title: 'Four possible endings', text: 'Seven nights lead to different truths. Your relationships and discoveries shape the final call.' },
]
