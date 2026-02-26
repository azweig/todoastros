// Servicio de música integrado en Next.js

interface Song {
  rank: number
  song: string
  artist: string
  date: string
}

interface MusicResponse {
  top_songs: Song[]
}

// Base de datos simulada de canciones populares por década
const popularSongsByDecade: Record<string, Song[]> = {
  "1960s": [
    { rank: 1, song: "I Want to Hold Your Hand", artist: "The Beatles", date: "1964-01-01" },
    { rank: 2, song: "(I Can't Get No) Satisfaction", artist: "The Rolling Stones", date: "1965-06-01" },
    { rank: 3, song: "Good Vibrations", artist: "The Beach Boys", date: "1966-10-01" },
    { rank: 4, song: "Respect", artist: "Aretha Franklin", date: "1967-04-01" },
    { rank: 5, song: "Hey Jude", artist: "The Beatles", date: "1968-08-01" },
  ],
  "1970s": [
    { rank: 1, song: "Stairway to Heaven", artist: "Led Zeppelin", date: "1971-11-01" },
    { rank: 2, song: "Bohemian Rhapsody", artist: "Queen", date: "1975-10-01" },
    { rank: 3, song: "Hotel California", artist: "Eagles", date: "1977-02-01" },
    { rank: 4, song: "Stayin' Alive", artist: "Bee Gees", date: "1977-12-01" },
    { rank: 5, song: "Imagine", artist: "John Lennon", date: "1971-10-01" },
  ],
  "1980s": [
    { rank: 1, song: "Billie Jean", artist: "Michael Jackson", date: "1983-01-01" },
    { rank: 2, song: "Sweet Child O' Mine", artist: "Guns N' Roses", date: "1988-08-01" },
    { rank: 3, song: "Like a Prayer", artist: "Madonna", date: "1989-03-01" },
    { rank: 4, song: "Every Breath You Take", artist: "The Police", date: "1983-05-01" },
    { rank: 5, song: "With or Without You", artist: "U2", date: "1987-03-01" },
  ],
  "1990s": [
    { rank: 1, song: "Smells Like Teen Spirit", artist: "Nirvana", date: "1991-09-01" },
    { rank: 2, song: "Wonderwall", artist: "Oasis", date: "1995-10-01" },
    { rank: 3, song: "...Baby One More Time", artist: "Britney Spears", date: "1998-10-01" },
    { rank: 4, song: "Nothing Compares 2 U", artist: "Sinéad O'Connor", date: "1990-01-01" },
    { rank: 5, song: "Vogue", artist: "Madonna", date: "1990-03-01" },
  ],
  "2000s": [
    { rank: 1, song: "Crazy In Love", artist: "Beyoncé ft. Jay-Z", date: "2003-05-01" },
    { rank: 2, song: "Hey Ya!", artist: "OutKast", date: "2003-09-01" },
    { rank: 3, song: "Umbrella", artist: "Rihanna ft. Jay-Z", date: "2007-03-01" },
    { rank: 4, song: "Toxic", artist: "Britney Spears", date: "2004-01-01" },
    { rank: 5, song: "Rolling in the Deep", artist: "Adele", date: "2010-11-01" },
  ],
  "2010s": [
    { rank: 1, song: "Uptown Funk", artist: "Mark Ronson ft. Bruno Mars", date: "2014-11-01" },
    { rank: 2, song: "Shape of You", artist: "Ed Sheeran", date: "2017-01-01" },
    { rank: 3, song: "Despacito", artist: "Luis Fonsi ft. Daddy Yankee", date: "2017-01-01" },
    { rank: 4, song: "Bad Guy", artist: "Billie Eilish", date: "2019-03-01" },
    { rank: 5, song: "Old Town Road", artist: "Lil Nas X ft. Billy Ray Cyrus", date: "2019-04-01" },
  ],
  "2020s": [
    { rank: 1, song: "Blinding Lights", artist: "The Weeknd", date: "2020-01-01" },
    { rank: 2, song: "Levitating", artist: "Dua Lipa", date: "2020-10-01" },
    { rank: 3, song: "Drivers License", artist: "Olivia Rodrigo", date: "2021-01-01" },
    { rank: 4, song: "As It Was", artist: "Harry Styles", date: "2022-04-01" },
    { rank: 5, song: "Flowers", artist: "Miley Cyrus", date: "2023-01-01" },
  ],
}

export function getPopularMusic(dateOfBirth: string): MusicResponse {
  const year = Number.parseInt(dateOfBirth.split("-")[0])
  let decade = "2020s"

  if (year < 1970) decade = "1960s"
  else if (year < 1980) decade = "1970s"
  else if (year < 1990) decade = "1980s"
  else if (year < 2000) decade = "1990s"
  else if (year < 2010) decade = "2000s"
  else if (year < 2020) decade = "2010s"

  // Obtener canciones de la década correspondiente
  const songs = popularSongsByDecade[decade]

  // Ajustar las fechas para que sean cercanas a la fecha de nacimiento
  const adjustedSongs = songs.map((song) => ({
    ...song,
    date: dateOfBirth, // Usar la fecha de nacimiento para simular que eran populares en ese momento
  }))

  return {
    top_songs: adjustedSongs,
  }
}

