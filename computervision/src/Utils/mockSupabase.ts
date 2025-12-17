// src/utils/mockSupabase.ts

export const mockSupabase = {
  signIn: async (email: string, password: string) => {
    await new Promise(r => setTimeout(r, 1000));
    if (email && password) return { user: { id: 'user-123', email }, error: null };
    return { user: null, error: { message: "Email/Password salah" } };
  },
  signUp: async (email: string, password: string) => {
    await new Promise(r => setTimeout(r, 1000));
    return { user: { id: 'user-123', email }, error: null };
  },
  from: (table: string) => {
    return {
      select: async () => {
        await new Promise(r => setTimeout(r, 500));
        const data = JSON.parse(localStorage.getItem('supabase_mock_mushrooms') || '[]');
        return { data, error: null };
      },
      insert: async (payload: any) => {
        await new Promise(r => setTimeout(r, 500));
        const current = JSON.parse(localStorage.getItem('supabase_mock_mushrooms') || '[]');
        const newItem = { ...payload[0], id: Date.now() }; 
        localStorage.setItem('supabase_mock_mushrooms', JSON.stringify([newItem, ...current]));
        return { error: null };
      },
      delete: () => ({
        eq: async (col: string, val: any) => {
             const current = JSON.parse(localStorage.getItem('supabase_mock_mushrooms') || '[]');
             const filtered = current.filter((item: any) => item.id !== val);
             localStorage.setItem('supabase_mock_mushrooms', JSON.stringify(filtered));
             return { error: null };
        }
      })
    };
  }
};