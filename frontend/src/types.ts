export interface RhymeInfo {
  perfect: string[];
  near: string[];
  slant: string[];
  span: [number, number];
}

export interface AnalyzeResponse {
  fragments: Record<string, RhymeInfo>;
  original_bar: string;
}

export type RhymeType = 'perfect' | 'near' | 'slant';