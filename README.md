# Content Planning Agency

A comprehensive AI-powered agency that creates strategic 1-week social media content plans for businesses across Facebook, Instagram, and LinkedIn.

## 🎯 Overview

The Content Planning Agency is a specialized multi-agent system that helps businesses create strategic, brand-aligned social media content plans. It collects business information and brand personality data, then generates comprehensive content strategies with detailed daily posts, visual concepts, and hashtag recommendations.

## ✨ Features

### Core Capabilities
- **Business Information Collection**: Industry analysis, target audience profiling, business goals, and challenges
- **Brand Personality Assessment**: Voice, tone, values, and personality trait analysis
- **Platform Selection**: Choose from Facebook, Instagram, LinkedIn, or combinations
- **Strategic Content Planning**: 1-week content plans with 7 detailed daily posts
- **Visual Design Guidance**: Specific design suggestions and visual concepts
- **Hashtag Strategy**: Optimized hashtag combinations for maximum reach and engagement

### Content Plan Structure
Each daily post includes:
- **Goal**: Clear objective aligned with business goals
- **Type of Post**: Platform-optimized content format
- **Title**: Compelling, brand-aligned headlines
- **Caption**: Engaging copy that reflects brand voice
- **Visual Concept**: Specific design recommendations
- **Hashtags**: Strategic mix of popular and niche hashtags

## 🤖 Agency Architecture

### Agents

#### 1. Content Strategist (Primary Interface)
- **Role**: Client interface and strategic coordination
- **Tools**: 5 specialized tools for business analysis and strategy
- **Responsibilities**: Information collection, strategic analysis, coordination

#### 2. Content Creator
- **Role**: Daily content generation and calendar assembly
- **Tools**: 3 tools for content creation and optimization
- **Responsibilities**: Post generation, content type optimization, calendar building

#### 3. Visual Designer
- **Role**: Visual concept and design guidance
- **Tools**: 2 tools for visual analysis and concept generation
- **Responsibilities**: Brand visual analysis, design suggestions, platform optimization

#### 4. Hashtag Researcher
- **Role**: Hashtag strategy and platform optimization
- **Tools**: 2 tools for hashtag research and platform optimization
- **Responsibilities**: Hashtag research, trend analysis, platform compliance

### Communication Flow
```
Content Strategist (User Interface)
    ↓
Content Creator (Content Generation)
    ↓
Visual Designer + Hashtag Researcher (Specialized Support)
    ↓
Content Creator (Final Assembly)
    ↓
Content Strategist (Strategy Summary & Delivery)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd content-plan-agency
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the agency**
```bash
python agency.py
```

### Getting Your OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in to your account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

## 📋 Usage

### Starting a Content Planning Session

1. **Launch the agency**
```bash
python agency.py
```

2. **Begin with business information collection**
The Content Strategist will guide you through:
   - Industry and business context
   - Target audience characteristics
   - Business goals and challenges
   - Brand personality assessment
   - Platform selection

3. **Receive your content plan**
The agency will deliver:
   - Complete 7-day content calendar
   - Strategic summary and recommendations
   - Implementation guidelines
   - Performance tracking metrics

### Example Workflow

```
User: "I need a content plan for my tech startup"

Content Strategist: "I'll help you create a comprehensive content plan. Let me start by collecting some information about your business..."

[Collects business info, brand personality, platform preferences]

Content Strategist: "Based on your information, I'll now coordinate with our content creation team..."

[Generates 7-day content plan with detailed posts]

Content Strategist: "Here's your complete content plan with strategy summary..."
```

## 🛠️ Technical Details

### Tools Overview (16 Total)

#### Content Strategist Tools (5)
- `BusinessIntakeCollector`: Collects comprehensive business information
- `BrandPersonalityAssessor`: Analyzes brand voice, tone, and values
- `PlatformSelector`: Manages platform selection and priorities
- `ContentStrategyAnalyzer`: Creates strategic framework
- `StrategySummaryGenerator`: Generates comprehensive summaries

#### Content Creator Tools (3)
- `DailyPostGenerator`: Creates detailed daily content
- `ContentTypeOptimizer`: Determines optimal post types
- `ContentCalendarBuilder`: Assembles complete calendar

#### Visual Designer Tools (2)
- `VisualConceptGenerator`: Creates design suggestions
- `BrandVisualAnalyzer`: Analyzes brand visual identity

#### Hashtag Researcher Tools (2)
- `HashtagResearchEngine`: Researches and recommends hashtags
- `PlatformHashtagOptimizer`: Optimizes for platform compliance

### Framework
- **Agency Swarm v1.0.1**: Multi-agent orchestration framework
- **OpenAI GPT-5**: Advanced language model for all agents
- **Pydantic**: Data validation and type safety
- **JSON**: Structured data exchange between agents

## 📊 Output Format

### Complete Content Plan Structure
```json
{
  "calendar_overview": {
    "total_posts": 7,
    "platforms_covered": ["Instagram", "LinkedIn"],
    "content_themes": ["Educational", "Behind-the-Scenes", "Problem-Solution"],
    "calendar_period": "1 week"
  },
  "daily_posts": [
    {
      "day": 1,
      "day_name": "Monday",
      "platform": "Instagram",
      "goal": "Increase brand awareness",
      "type_of_post": "Image Post",
      "title": "How to Optimize Your Social Media Strategy",
      "caption": "Did you know that... [engaging caption]",
      "visual_concept": "Clean infographic with brand colors",
      "hashtags": ["#business", "#marketing", "#entrepreneur"],
      "brand_alignment": {
        "voice": "Professional and authoritative",
        "tone": "Encouraging and supportive"
      }
    }
    // ... 6 more daily posts
  ],
  "strategy_summary": {
    "executive_summary": "Comprehensive overview of strategy",
    "implementation_guidance": "Step-by-step implementation",
    "success_metrics": "KPIs and tracking recommendations"
  }
}
```

## 🎨 Customization

### Brand Alignment
- All content reflects established brand personality
- Visual concepts align with brand identity
- Hashtag strategy supports brand voice

### Platform Optimization
- Facebook: Community-focused, 1-3 hashtags
- Instagram: Visual-first, 5-15 hashtags
- LinkedIn: Professional, 3-5 hashtags

### Industry Adaptation
- Technology: Innovation and trends focus
- Healthcare: Trust-building and education
- E-commerce: Product showcase and social proof
- Professional Services: Thought leadership

## 📈 Success Metrics

### Primary KPIs
- Engagement rate improvement
- Reach and impressions growth
- Lead generation and conversion metrics
- Brand awareness and recognition

### Content Performance
- Post engagement rates by platform
- Content type performance analysis
- Hashtag effectiveness tracking
- Audience growth and retention

## 🔧 Development

### Project Structure
```
content-plan-agency/
├── content_strategist/
│   ├── tools/
│   ├── files/
│   └── instructions.md
├── content_creator/
│   ├── tools/
│   ├── files/
│   └── instructions.md
├── visual_designer/
│   ├── tools/
│   ├── files/
│   └── instructions.md
├── hashtag_researcher/
│   ├── tools/
│   ├── files/
│   └── instructions.md
├── agency.py
├── shared_instructions.md
├── requirements.txt
└── README.md
```

### Adding New Features
1. Create new tools in appropriate agent folders
2. Update agent instructions for new capabilities
3. Modify communication flows in `agency.py`
4. Test thoroughly before deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the example usage

## 🔮 Future Enhancements

- Integration with social media scheduling tools
- Real-time hashtag trend monitoring
- A/B testing recommendations
- Advanced analytics integration
- Multi-language support
- Custom industry templates

---

**Built with Agency Swarm v1.0.1** - The powerful framework for creating collaborative AI agent systems.