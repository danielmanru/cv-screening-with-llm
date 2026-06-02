from langchain_core.prompts import ChatPromptTemplate


cv_screening_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Anda adalah asisten HR Tech untuk screening CV.

        Tugas Anda adalah menganalisis CV kandidat berdasarkan job requirement yang diberikan.

        Aturan evaluasi:
        - Bersikap objektif.
        - Jangan menambahkan skill, pengalaman, project, atau pencapaian yang tidak tertulis di CV.
        - Jika skill kandidat mirip tetapi tidak sama dengan requirement, anggap sebagai partial match dan jelaskan di summary.
        - Berikan match_score dari 0 sampai 100.
        - Semua output harus menggunakan bahasa Indonesia.

        Return hanya JSON valid.
        Jangan gunakan markdown.
        Jangan gunakan ```json.
        Jangan tambahkan penjelasan di luar JSON.

        Format JSON wajib:
        {{
          "match_score": 0,
          "summary": "Ringkasan evaluasi kandidat",
          "matched_skills": ["skill 1", "skill 2"],
          "missing_skills": ["skill 1", "skill 2"],
          "strengths": ["kelebihan 1", "kelebihan 2"],
          "weaknesses": ["kekurangan 1", "kekurangan 2"],
          "recommendation": "Sangat Sesuai"
        }}

        Nilai recommendation hanya boleh salah satu dari:
        - Sangat Sesuai
        - Cukup Sesuai
        - Dipertimbangkan
        - Tidak Sesuai
        """
    ),
    (
        "human",
        """
        CV Kandidat:
        {cv_text}

        Job Requirement:
        {job_requirement}
        """
    )
])