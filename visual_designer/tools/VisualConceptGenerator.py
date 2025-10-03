from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class VisualConceptGenerator(BaseTool):
    """
    Creates specific design suggestions and visual concepts for each content post,
    ensuring visual elements align with brand identity and platform best practices.
    """
    
    post_content: Dict[str, Any] = Field(
        ..., description="Complete post details including title, caption, and context"
    )
    brand_colors: str = Field(
        ..., description="Brand color palette (e.g., 'Primary: #1E40AF, Secondary: #F59E0B, Accent: #10B981')"
    )
    brand_style: str = Field(
        ..., description="Brand visual style preferences (e.g., 'Modern and minimal', 'Professional and clean', 'Bold and energetic')"
    )
    platform: str = Field(
        ..., description="Target social media platform (Facebook, Instagram, LinkedIn)"
    )
    content_type: str = Field(
        ..., description="Type of content (Image Post, Video, Story, Reel, etc.)"
    )

    def run(self):
        """
        Generates detailed visual concept with specific design recommendations.
        """
        # Step 1: Validate inputs
        if not self.post_content or not self.brand_colors:
            return "Error: Post content and brand colors are required."
        
        # Step 2: Get additional context from agency context
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        
        if not all([business_data, brand_personality]):
            return "Error: Missing required context data. Please ensure business data and brand personality are available."
        
        # Step 3: Generate visual concept
        visual_concept = self._generate_visual_concept(
            business_data, brand_personality
        )
        
        # Step 4: Store visual concept in context
        post_key = f"visual_concept_{self.post_content.get('day', 'unknown')}"
        self._context.set(post_key, visual_concept)
        
        # Step 5: Return detailed visual concept
        return json.dumps({
            "status": "success",
            "message": "Visual concept generated successfully",
            "visual_concept": visual_concept
        }, indent=2)

    def _generate_visual_concept(self, business_data: Dict, brand_personality: Dict) -> Dict[str, Any]:
        """Generates comprehensive visual concept based on post and brand context"""
        
        # Step 1: Analyze brand personality for visual translation
        brand_visual_analysis = self._analyze_brand_visual_identity(
            brand_personality, business_data["industry"]
        )
        
        # Step 2: Create platform-specific design recommendations
        platform_design = self._create_platform_specific_design(
            self.platform, self.content_type
        )
        
        # Step 3: Generate specific design suggestions
        design_suggestions = self._generate_design_suggestions(
            self.post_content, brand_visual_analysis, platform_design
        )
        
        # Step 4: Create color palette recommendations
        color_recommendations = self._create_color_recommendations(
            self.brand_colors, brand_visual_analysis
        )
        
        # Step 5: Generate layout and composition suggestions
        layout_suggestions = self._generate_layout_suggestions(
            self.content_type, self.platform, brand_visual_analysis
        )
        
        # Step 6: Create typography recommendations
        typography_recommendations = self._create_typography_recommendations(
            brand_personality, self.platform
        )
        
        return {
            "post_context": {
                "day": self.post_content.get("day"),
                "title": self.post_content.get("title"),
                "content_theme": self.post_content.get("content_theme"),
                "goal": self.post_content.get("goal")
            },
            "brand_visual_identity": brand_visual_analysis,
            "platform_specifications": platform_design,
            "design_concept": design_suggestions,
            "color_palette": color_recommendations,
            "layout_composition": layout_suggestions,
            "typography": typography_recommendations,
            "visual_elements": self._recommend_visual_elements(
                self.post_content, brand_visual_analysis
            ),
            "implementation_notes": self._create_implementation_notes(
                self.platform, self.content_type
            )
        }

    def _analyze_brand_visual_identity(self, brand_personality: Dict, industry: str) -> Dict[str, Any]:
        """Analyzes brand personality to determine appropriate visual style"""
        
        voice = brand_personality["brand_voice"].lower()
        tone = brand_personality["brand_tone"].lower()
        values = brand_personality["core_values"].lower()
        
        # Determine visual personality
        visual_personality = "balanced"
        if "professional" in voice or "formal" in voice:
            visual_personality = "professional"
        elif "casual" in voice or "friendly" in voice:
            visual_personality = "approachable"
        elif "playful" in voice or "energetic" in voice:
            visual_personality = "dynamic"
        
        # Determine mood and atmosphere
        mood = "neutral"
        if "warm" in tone or "supportive" in tone:
            mood = "warm"
        elif "confident" in tone or "bold" in tone:
            mood = "confident"
        elif "encouraging" in tone:
            mood = "uplifting"
        
        # Industry-specific visual considerations
        industry_considerations = {
            "technology": {
                "style_preferences": ["Clean lines", "Modern typography", "Tech-inspired graphics"],
                "avoid": ["Overly decorative elements", "Outdated design patterns"]
            },
            "healthcare": {
                "style_preferences": ["Clean and sterile", "Trust-building imagery", "Professional photography"],
                "avoid": ["Overly flashy designs", "Unprofessional imagery"]
            },
            "e-commerce": {
                "style_preferences": ["Product-focused", "Lifestyle imagery", "Clear call-to-actions"],
                "avoid": ["Cluttered layouts", "Poor product photography"]
            }
        }
        
        industry_guidelines = industry_considerations.get(
            industry.lower(), 
            industry_considerations["technology"]
        )
        
        return {
            "visual_personality": visual_personality,
            "mood": mood,
            "style_characteristics": self._determine_style_characteristics(visual_personality, mood),
            "industry_guidelines": industry_guidelines,
            "brand_values_reflection": self._translate_values_to_visual(values)
        }

    def _determine_style_characteristics(self, visual_personality: str, mood: str) -> List[str]:
        """Determines specific style characteristics based on personality and mood"""
        
        characteristics = {
            "professional": {
                "warm": ["Clean layouts", "Professional typography", "Warm color accents"],
                "confident": ["Bold typography", "Strong compositions", "High contrast"],
                "uplifting": ["Positive imagery", "Bright accents", "Encouraging visuals"],
                "neutral": ["Balanced compositions", "Professional imagery", "Clean design"]
            },
            "approachable": {
                "warm": ["Friendly imagery", "Rounded elements", "Inviting colors"],
                "confident": ["Strong but friendly", "Approachable authority", "Warm professionalism"],
                "uplifting": ["Positive messaging", "Bright and cheerful", "Community-focused"],
                "neutral": ["Friendly professional", "Approachable design", "Welcoming aesthetic"]
            },
            "dynamic": {
                "warm": ["Energetic but warm", "Vibrant colors", "Active imagery"],
                "confident": ["Bold and energetic", "Strong visual impact", "Dynamic compositions"],
                "uplifting": ["High energy", "Motivational visuals", "Vibrant and positive"],
                "neutral": ["Dynamic but balanced", "Energetic design", "Active visual style"]
            }
        }
        
        return characteristics.get(visual_personality, {}).get(mood, ["Balanced design", "Professional approach"])

    def _translate_values_to_visual(self, values: str) -> Dict[str, str]:
        """Translates brand values into visual recommendations"""
        
        value_translations = {
            "innovation": "Modern design elements, forward-thinking visuals, creative layouts",
            "quality": "High-resolution imagery, premium feel, attention to detail",
            "trust": "Professional photography, consistent branding, authentic imagery",
            "customer-first": "People-focused imagery, customer testimonials, service-oriented visuals",
            "transparency": "Clean layouts, honest imagery, straightforward design",
            "sustainability": "Natural colors, eco-friendly imagery, green elements",
            "community": "Group imagery, collaborative visuals, inclusive design",
            "excellence": "Premium design, high-quality imagery, refined aesthetics"
        }
        
        visual_recommendations = []
        for value_key, translation in value_translations.items():
            if value_key in values.lower():
                visual_recommendations.append(translation)
        
        return {
            "primary_visual_themes": visual_recommendations[:3],
            "design_priorities": "Focus on visual elements that reinforce core brand values"
        }

    def _create_platform_specific_design(self, platform: str, content_type: str) -> Dict[str, Any]:
        """Creates platform-specific design recommendations"""
        
        platform_specs = {
            "Facebook": {
                "image_dimensions": {
                    "feed_post": "1200x630px",
                    "story": "1080x1920px",
                    "cover_photo": "1200x315px"
                },
                "design_considerations": [
                    "Text overlay should be readable on mobile",
                    "Use high contrast for better visibility",
                    "Consider how content appears in news feed",
                    "Include clear call-to-action elements"
                ],
                "optimal_formats": ["JPEG", "PNG"],
                "text_guidelines": "Keep text minimal, use large fonts for mobile viewing"
            },
            "Instagram": {
                "image_dimensions": {
                    "feed_post": "1080x1080px (square) or 1080x1350px (portrait)",
                    "story": "1080x1920px",
                    "reel": "1080x1920px"
                },
                "design_considerations": [
                    "High visual impact is crucial",
                    "Use vibrant colors and high contrast",
                    "Ensure mobile-first design",
                    "Consider Instagram's visual aesthetic"
                ],
                "optimal_formats": ["JPEG", "PNG", "MP4"],
                "text_guidelines": "Minimal text overlay, let visuals speak"
            },
            "LinkedIn": {
                "image_dimensions": {
                    "feed_post": "1200x627px",
                    "article_cover": "1200x627px",
                    "company_logo": "300x300px"
                },
                "design_considerations": [
                    "Professional and clean aesthetic",
                    "Business-appropriate imagery",
                    "Clear, readable text",
                    "Professional color schemes"
                ],
                "optimal_formats": ["JPEG", "PNG"],
                "text_guidelines": "Professional typography, clear messaging"
            }
        }
        
        platform_config = platform_specs.get(platform, platform_specs["Facebook"])
        
        # Add content-type specific recommendations
        content_type_recommendations = self._get_content_type_recommendations(content_type, platform)
        
        return {
            "platform": platform,
            "content_type": content_type,
            "dimensions": platform_config["image_dimensions"].get(
                content_type.lower().replace(" ", "_"), 
                list(platform_config["image_dimensions"].values())[0]
            ),
            "design_considerations": platform_config["design_considerations"],
            "content_type_specific": content_type_recommendations,
            "optimal_formats": platform_config["optimal_formats"],
            "text_guidelines": platform_config["text_guidelines"]
        }

    def _get_content_type_recommendations(self, content_type: str, platform: str) -> List[str]:
        """Gets content-type specific design recommendations"""
        
        recommendations = {
            "image_post": [
                "Use high-quality, eye-catching imagery",
                "Ensure proper composition and focal point",
                "Consider rule of thirds for layout"
            ],
            "video": [
                "Create engaging thumbnail image",
                "Use captions for accessibility",
                "Keep opening 3 seconds compelling"
            ],
            "story": [
                "Design for vertical viewing",
                "Use bold, readable text",
                "Create immersive, full-screen experience"
            ],
            "reel": [
                "Design for vertical, mobile-first viewing",
                "Create hook in first 3 seconds",
                "Use trending audio and effects"
            ],
            "carousel": [
                "Design cohesive visual story across slides",
                "Use consistent branding elements",
                "Create clear progression and narrative"
            ]
        }
        
        return recommendations.get(content_type.lower().replace(" ", "_"), recommendations["image_post"])

    def _generate_design_suggestions(self, post_content: Dict, brand_visual_analysis: Dict, 
                                   platform_design: Dict) -> Dict[str, Any]:
        """Generates specific design suggestions for the post"""
        
        content_theme = post_content.get("content_theme", "General")
        goal = post_content.get("goal", "")
        
        # Theme-based design suggestions
        theme_designs = {
            "Educational Content": {
                "visual_approach": "Clean, informative layout with clear hierarchy",
                "key_elements": ["Infographic elements", "Step-by-step visuals", "Data visualization"],
                "composition": "Use grids and structured layouts for easy reading"
            },
            "Behind-the-Scenes": {
                "visual_approach": "Authentic, candid photography with natural lighting",
                "key_elements": ["Team photos", "Process shots", "Workspace imagery"],
                "composition": "Use documentary-style photography with natural compositions"
            },
            "Problem-Solution": {
                "visual_approach": "Before/after comparisons or solution-focused imagery",
                "key_elements": ["Comparison visuals", "Solution highlights", "Benefit demonstrations"],
                "composition": "Use split-screen or sequential layouts"
            }
        }
        
        theme_design = theme_designs.get(content_theme, theme_designs["Educational Content"])
        
        # Goal-based design adjustments
        goal_adjustments = {
            "engagement": "Include interactive elements, questions, or polls in visual",
            "education": "Focus on clear, readable information hierarchy",
            "awareness": "Use bold, memorable visuals with strong brand presence",
            "conversion": "Include clear call-to-action elements and benefit highlights"
        }
        
        goal_adjustment = ""
        for goal_key, adjustment in goal_adjustments.items():
            if goal_key in goal.lower():
                goal_adjustment = adjustment
                break
        
        return {
            "overall_approach": theme_design["visual_approach"],
            "key_visual_elements": theme_design["key_elements"],
            "composition_guidelines": theme_design["composition"],
            "goal_specific_adjustments": goal_adjustment,
            "brand_alignment": brand_visual_analysis["style_characteristics"],
            "platform_optimization": platform_design["design_considerations"]
        }

    def _create_color_recommendations(self, brand_colors: str, brand_visual_analysis: Dict) -> Dict[str, Any]:
        """Creates detailed color palette recommendations"""
        
        # Parse brand colors
        color_palette = self._parse_brand_colors(brand_colors)
        
        # Determine color usage recommendations
        color_usage = {
            "primary_color": {
                "usage": "Main brand elements, headlines, key focal points",
                "percentage": "40-60% of design"
            },
            "secondary_color": {
                "usage": "Supporting elements, accents, call-to-action buttons",
                "percentage": "20-30% of design"
            },
            "accent_color": {
                "usage": "Highlights, important elements, attention-grabbers",
                "percentage": "10-20% of design"
            }
        }
        
        # Add mood-based color adjustments
        mood_adjustments = {
            "warm": "Use warmer tones and softer color transitions",
            "confident": "Use high contrast and bold color combinations",
            "uplifting": "Incorporate bright, energetic accent colors",
            "neutral": "Maintain balanced color distribution"
        }
        
        mood = brand_visual_analysis.get("mood", "neutral")
        mood_adjustment = mood_adjustments.get(mood, "Maintain brand color consistency")
        
        return {
            "brand_color_palette": color_palette,
            "color_usage_guidelines": color_usage,
            "mood_based_adjustments": mood_adjustment,
            "contrast_recommendations": "Ensure sufficient contrast for accessibility (WCAG AA standards)",
            "color_psychology": self._explain_color_psychology(color_palette)
        }

    def _parse_brand_colors(self, brand_colors: str) -> Dict[str, str]:
        """Parses brand color string into structured palette"""
        
        # Simple parsing - can be enhanced based on input format
        color_palette = {}
        
        # Look for common color patterns
        import re
        color_pattern = r'#([A-Fa-f0-9]{6})'
        colors = re.findall(color_pattern, brand_colors)
        
        if colors:
            color_palette["primary"] = f"#{colors[0]}"
            if len(colors) > 1:
                color_palette["secondary"] = f"#{colors[1]}"
            if len(colors) > 2:
                color_palette["accent"] = f"#{colors[2]}"
        
        # Fallback if no hex colors found
        if not color_palette:
            color_palette = {
                "primary": "#1E40AF",
                "secondary": "#F59E0B", 
                "accent": "#10B981"
            }
        
        return color_palette

    def _explain_color_psychology(self, color_palette: Dict[str, str]) -> Dict[str, str]:
        """Explains color psychology for the brand palette"""
        
        color_psychology = {
            "#1E40AF": "Blue - Trust, professionalism, stability",
            "#F59E0B": "Orange - Energy, enthusiasm, creativity", 
            "#10B981": "Green - Growth, harmony, success",
            "#EF4444": "Red - Urgency, passion, excitement",
            "#8B5CF6": "Purple - Luxury, creativity, wisdom",
            "#F59E0B": "Yellow - Optimism, clarity, warmth"
        }
        
        explanations = {}
        for color_name, color_code in color_palette.items():
            explanations[color_name] = color_psychology.get(color_code, "Professional and trustworthy")
        
        return explanations

    def _generate_layout_suggestions(self, content_type: str, platform: str, 
                                   brand_visual_analysis: Dict) -> Dict[str, Any]:
        """Generates layout and composition suggestions"""
        
        layout_recommendations = {
            "composition_principles": [
                "Use rule of thirds for focal points",
                "Maintain visual hierarchy with size and contrast",
                "Create balanced negative space",
                "Ensure mobile-first design principles"
            ],
            "layout_structure": self._recommend_layout_structure(content_type, platform),
            "visual_hierarchy": self._create_visual_hierarchy_guidelines(),
            "spacing_guidelines": self._create_spacing_guidelines(platform),
            "responsive_considerations": self._create_responsive_guidelines(platform)
        }
        
        return layout_recommendations

    def _recommend_layout_structure(self, content_type: str, platform: str) -> str:
        """Recommends specific layout structure for content type"""
        
        structures = {
            "image_post": "Single focal point with supporting text overlay",
            "video": "Thumbnail with engaging opening frame and clear title",
            "story": "Full-screen vertical layout with clear messaging hierarchy",
            "carousel": "Cohesive story progression across multiple slides"
        }
        
        return structures.get(content_type.lower().replace(" ", "_"), "Balanced composition with clear focal point")

    def _create_visual_hierarchy_guidelines(self) -> List[str]:
        """Creates guidelines for visual hierarchy"""
        
        return [
            "Most important element should be largest and most prominent",
            "Use color contrast to create emphasis",
            "Maintain consistent spacing between elements",
            "Ensure text is readable at all sizes",
            "Create clear path for eye movement through design"
        ]

    def _create_spacing_guidelines(self, platform: str) -> Dict[str, str]:
        """Creates spacing guidelines for platform"""
        
        spacing_guidelines = {
            "Facebook": "Use generous padding, especially for mobile viewing",
            "Instagram": "Tighter spacing acceptable, focus on visual impact",
            "LinkedIn": "Professional spacing, clean and organized layout"
        }
        
        return {
            "platform_specific": spacing_guidelines.get(platform, "Balanced spacing for optimal readability"),
            "general_principles": "Maintain consistent spacing throughout design"
        }

    def _create_responsive_guidelines(self, platform: str) -> List[str]:
        """Creates responsive design guidelines"""
        
        return [
            "Design for mobile-first viewing experience",
            "Ensure text remains readable at small sizes",
            "Test design on multiple screen sizes",
            "Consider how design appears in feed context"
        ]

    def _create_typography_recommendations(self, brand_personality: Dict, platform: str) -> Dict[str, Any]:
        """Creates typography recommendations based on brand personality"""
        
        voice = brand_personality["brand_voice"].lower()
        
        # Determine typography style
        if "professional" in voice or "formal" in voice:
            typography_style = "Professional and clean"
            font_characteristics = ["Sans-serif fonts", "High readability", "Conservative styling"]
        elif "casual" in voice or "friendly" in voice:
            typography_style = "Approachable and friendly"
            font_characteristics = ["Rounded fonts", "Warm feel", "Inviting typography"]
        elif "playful" in voice or "energetic" in voice:
            typography_style = "Dynamic and energetic"
            font_characteristics = ["Bold fonts", "High impact", "Expressive typography"]
        else:
            typography_style = "Balanced and versatile"
            font_characteristics = ["Readable fonts", "Professional with personality", "Flexible styling"]
        
        return {
            "typography_style": typography_style,
            "font_characteristics": font_characteristics,
            "hierarchy_guidelines": [
                "Use 2-3 font sizes maximum",
                "Maintain consistent font weights",
                "Ensure sufficient contrast between text and background",
                "Use appropriate line spacing for readability"
            ],
            "platform_considerations": self._get_platform_typography_guidelines(platform)
        }

    def _get_platform_typography_guidelines(self, platform: str) -> List[str]:
        """Gets platform-specific typography guidelines"""
        
        guidelines = {
            "Facebook": [
                "Keep text overlay minimal and readable",
                "Use larger fonts for mobile viewing",
                "Ensure text doesn't compete with image"
            ],
            "Instagram": [
                "Minimize text overlay on images",
                "Use bold, readable fonts for Stories",
                "Consider text in captions rather than on image"
            ],
            "LinkedIn": [
                "Use professional, clean typography",
                "Maintain business-appropriate font choices",
                "Ensure readability in professional context"
            ]
        }
        
        return guidelines.get(platform, ["Ensure readability across all devices"])

    def _recommend_visual_elements(self, post_content: Dict, brand_visual_analysis: Dict) -> List[Dict[str, str]]:
        """Recommends specific visual elements for the post"""
        
        content_theme = post_content.get("content_theme", "General")
        
        visual_elements = {
            "Educational Content": [
                {"element": "Infographic icons", "purpose": "Visual data representation"},
                {"element": "Step indicators", "purpose": "Process clarity"},
                {"element": "Chart/graph elements", "purpose": "Data visualization"}
            ],
            "Behind-the-Scenes": [
                {"element": "Candid photography", "purpose": "Authentic storytelling"},
                {"element": "Team member photos", "purpose": "Human connection"},
                {"element": "Workspace imagery", "purpose": "Company culture"}
            ],
            "Problem-Solution": [
                {"element": "Before/after visuals", "purpose": "Clear comparison"},
                {"element": "Solution highlights", "purpose": "Benefit demonstration"},
                {"element": "Success indicators", "purpose": "Proof of effectiveness"}
            ]
        }
        
        return visual_elements.get(content_theme, [
            {"element": "Brand elements", "purpose": "Consistent branding"},
            {"element": "High-quality imagery", "purpose": "Professional appearance"}
        ])

    def _create_implementation_notes(self, platform: str, content_type: str) -> List[str]:
        """Creates implementation notes for designers"""
        
        return [
            "Ensure all text is readable at small sizes for mobile viewing",
            "Test design in actual platform context before finalizing",
            "Maintain brand consistency across all visual elements",
            "Consider accessibility guidelines for color contrast and text size",
            f"Optimize for {platform} best practices and user expectations",
            "Prepare multiple format variations if needed for different placements"
        ]

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = VisualConceptGenerator(
        post_content={
            "day": 1,
            "title": "How to Optimize Your Social Media Strategy",
            "content_theme": "Educational Content",
            "goal": "Educate audience about industry topics"
        },
        brand_colors="Primary: #1E40AF, Secondary: #F59E0B, Accent: #10B981",
        brand_style="Modern and professional",
        platform="Instagram",
        content_type="Image Post"
    )
    print(tool.run())
