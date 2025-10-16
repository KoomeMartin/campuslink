
export interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: Source[];
  suggestions?: Suggestion[];
  followUp?: string;
}

export interface Source {
  id: string;
  title: string;
  snippet: string;
  category: string;
}

export interface Suggestion {
  id: string;
  label: string;
  prompt: string;
}

export interface ChatRequest {
  message: string;
  user_profile?: {
    program?: string;
    year?: number;
  };
  session_id?: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  suggestions: Suggestion[];
  follow_up?: string;
}
