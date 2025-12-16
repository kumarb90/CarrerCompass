import re

SKILL_DICT = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "react": ["react", "reactjs"],
    "nodejs": ["node", "nodejs"],
    "aws": ["aws", "amazon web services", "lambda", "ec2", "s3"],
    "docker": ["docker", "containerization", "containers"],
    "mysql": ["mysql", "sql", "database"],
    "flask": ["flask"],
    "django": ["django"],
    "ml": ["machine learning", "ml"],
    "digital_marketing": ["digital marketing"],
    "social_media": ["social media", "instagram", "facebook", "linkedin", "twitter"],
    "content_creation": ["content creation", "content writing", "copywriting"],
    "seo": ["seo", "search engine optimization"],
    "marketing_strategy": ["marketing strategy", "marketing strategies"],
    "campaign_management": ["campaign", "campaigns", "marketing campaigns"],
    "market_research": ["market research", "consumer research"],
    "analytics": ["analytics", "data analysis", "campaign performance"],
    "communication": ["communication", "presentation", "verbal", "written"],
    "creativity": ["creativity", "creative"],
}


def extract_skills(text: str):
    text = text.lower()
    found = set()

    for canonical, keywords in SKILL_DICT.items():
        for k in keywords:
            if re.search(rf"\b{k}\b", text):
                found.add(canonical)
                break

    return list(found)
