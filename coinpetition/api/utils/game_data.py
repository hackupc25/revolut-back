"""
Game data module containing predefined lists for the situation generator.
Each list contains 50 realistic options related to current events and real-world scenarios.
"""

# 50 possible characters that can present events
TARGETS = [
    # Political figures
    "Tech Billionaire",
    "Populist President",
    "Climate Activist",
    "Wall Street Investor",
    "Central Bank Chair",
    "Social Media CEO",
    "Controversial Politician",
    "Nobel Prize Winner",
    "Famous Economist",
    "Whistleblower",
    "Influential Journalist",
    "Celebrity Activist",
    "Corporate Lobbyist",
    "Former Head of State",
    "Cryptocurrency Pioneer",
    
    # Celebrities and influencers
    "Pop Music Superstar",
    "Viral TikTok Creator",
    "Academy Award Winner",
    "Sports MVP",
    "Renowned Scientist",
    "Space Exploration Entrepreneur",
    "Gaming Industry Executive",
    "Reality TV Star",
    "Celebrity Chef",
    "Fashion Icon",
    "Bestselling Author",
    "Podcast Host",
    "Self-Help Guru",
    "Olympic Gold Medalist",
    "Media Conglomerate Owner",
    
    # Business and tech figures
    "AI Researcher",
    "Tech Startup Founder",
    "Investment Bank CEO",
    "Venture Capital Partner",
    "Labor Union Leader",
    "Financial Analyst",
    "Energy Company Executive",
    "Medical Research Director",
    "Pharmaceutical Company CEO",
    "Agricultural Industry Leader",
    "E-commerce Marketplace Founder",
    "Blockchain Developer",
    "Social Media Influencer",
    "Data Privacy Expert",
    "Quantum Computing Scientist"
]

# 50 possible areas where events occur
AREAS = [
    # Global locations
    "United Nations Headquarters",
    "Wall Street Trading Floor",
    "Silicon Valley Campus",
    "International Summit",
    "Global Economic Forum",
    "Major Tech Conference",
    "Military Base",
    "Political Campaign Rally",
    "Stock Exchange Floor",
    "Corporate Boardroom",
    "Space Agency Launch Site",
    "Climate Conference",
    "International Border",
    "Global Health Organization HQ",
    "Financial District",
    
    # Event venues and social contexts
    "Viral Social Media Platform",
    "Streaming Service Premiere",
    "Celebrity Award Ceremony",
    "Prestigious University",
    "Olympic Stadium",
    "Protest Demonstration",
    "Charity Fundraiser Gala",
    "Fashion Week Runway",
    "Television News Studio",
    "Podcast Recording Studio",
    "Agricultural Fair",
    "Music Festival",
    "Film Festival",
    "Political Debate Stage",
    "Scientific Research Lab",
    
    # Other relevant settings
    "Cryptocurrency Exchange",
    "Blockchain Conference",
    "Manufacturing Plant",
    "Retail Store Chain",
    "AI Research Center",
    "Hospital System",
    "Urban City Center",
    "Rural Community",
    "Energy Production Facility",
    "International Airport Hub",
    "Government Intelligence Agency",
    "Courthouse",
    "Legislative Chamber",
    "Multinational Corporation HQ",
    "Renewable Energy Farm",
    "Diplomatic Embassy",
    "Sports Championship",
    "Crowdfunding Platform",
    "E-sports Tournament",
    "Cultural Heritage Site"
]

# 50 possible types of events
EVENT_TYPES = [
    # Market and economic events
    "Market Crash",
    "IPO Launch",
    "Central Bank Interest Rate Decision",
    "Cryptocurrency Regulation Announcement",
    "Unexpected Inflation Report",
    "Stock Market Rally",
    "Major Corporate Merger",
    "Supply Chain Disruption",
    "Tech Company Data Breach",
    "Global Trade Agreement",
    "Currency Devaluation",
    "Economic Sanctions",
    "Commodity Price Shock",
    "Retail Spending Report",
    "Housing Market Shift",
    
    # Political and geopolitical events
    "Election Results",
    "Political Scandal",
    "Military Conflict Outbreak",
    "Peace Treaty Signing",
    "Diplomatic Crisis",
    "Policy Reform Announcement",
    "Government Shutdown",
    "Climate Agreement",
    "Constitutional Challenge",
    "Leadership Change",
    "Protest Movement",
    "Legislative Gridlock",
    "Whistleblower Revelation",
    "International Summit Decision",
    "Border Dispute",
    
    # Technology and cultural events
    "Breakthrough Scientific Discovery",
    "Viral Social Media Trend",
    "Major Product Launch",
    "Celebrity Controversy",
    "Cybersecurity Attack",
    "AI Advancement Announcement",
    "Space Exploration Milestone",
    "Global Health Emergency",
    "Renewable Energy Breakthrough",
    "Sports Championship Upset",
    "Award Show Controversy",
    "Food Safety Recall",
    "Agricultural Harvest Report",
    "Manufacturing Output Data",
    "Entertainment Industry Strike",
    "Streaming Platform Content Deal",
    "Media Company Acquisition",
    "Environmental Disaster",
    "Transportation Industry Disruption",
    "Labor Market Report"
] 