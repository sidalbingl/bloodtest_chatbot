const API_BASE_URL = 'http://localhost:8000';

export interface Message {
  text: string;
  isUser: boolean;
}

export interface AnalysisResult {
  id: string;
  date: string;
  fileName: string;
  results: Record<string, any>;
  summary: string;
}

export const uploadFile = async (file: File): Promise<AnalysisResult> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Dosya yükleme hatası');
    }

    return response.json();
  } catch (error) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error('Backend sunucusuna bağlanılamadı. Lütfen backend sunucusunun çalıştığından emin olun.');
    }
    throw error;
  }
};

export const sendMessage = async (message: string): Promise<string> => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: message }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Mesaj gönderme hatası');
  }

  const data = await response.json();
  return data.response;
};

export const getHistory = async (): Promise<AnalysisResult[]> => {
  const response = await fetch(`${API_BASE_URL}/history`);

  if (!response.ok) {
    throw new Error('Geçmiş getirme hatası');
  }

  const data = await response.json();
  return data.history;
}; 