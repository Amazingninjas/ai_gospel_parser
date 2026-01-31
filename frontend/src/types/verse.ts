export interface VerseWord {
  greek: string;
  transliteration: string;
  strongs_number: string;
  morphology: string;
  english: string;
}

export interface Verse {
  reference: string;
  book: string;
  chapter: number;
  verse: number;
  greek_text: string;
  english_text: string;
  words?: VerseWord[];
}

export interface Book {
  code: string;
  name: string;
  chapters: number;
}
