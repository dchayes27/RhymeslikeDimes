export interface RhymeInfo {
  perfect: string[];
  near: string[];
  slant: string[];
  phrase_perfect: string[];
  phrase_near: string[];
  phrase_slant: string[];
  span: [number, number];
}

export interface AnalyzeResponse {
  fragments: Record<string, RhymeInfo>;
  original_bar: string;
}

export type RhymeType = Exclude<keyof RhymeInfo, 'span'>;
