from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any, List

class BrandVisualAnalyzer(BaseTool):
    """
    Analyzes brand identity to determine appropriate visual style and design elements
    that align with brand personality and industry standards.
    """
    
    brand_personality: Dict[str, Any] = Field(
        ..., description="Complete brand personality profile including voice, tone, and values"
    )
    industry: str = Field(
        ..., description="Business industry context for visual style determination"
    )
    target_audience: str = Field(
        ..., description="Audience characteristics for visual preference analysis"
    )

    def run(self):
        """
        Analyzes brand personality and context to create comprehensive visual guidelines.
        """
        # Step 1: Validate inputs
        if not self.brand_personality or not self.industry:
            return "Error: Brand personality and industry are required."
        
        # Step 2: Get additional context from agency context
        business_data = self._context.get("business_data")
        
        if not business_data:
            return "Error: Missing business data context. Please ensure business intake is completed."
        
        # Step 3: Perform comprehensive brand visual analysis
        visual_analysis = self._perform_brand_visual_analysis()
        
        # Step 4: Store visual guidelines in context
        self._context.set("brand_visual_guidelines", visual_analysis)
        
        # Step 5: Return comprehensive visual analysis
        return json.dumps({
            "status": "success",
            "message": "Brand visual analysis completed successfully",
            "visual_analysis": visual_analysis
        }, indent=2)

    def _perform_brand_visual_analysis(self) -> Dict[str, Any]:
        """Performs comprehensive brand visual analysis"""
        
        # Step 1: Analyze brand personality for visual translation
        personality_analysis = self._analyze_personality_for_visuals()
        
        # Step 2: Determine industry-appropriate visual standards
        industry_standards = self._determine_industry_visual_standards()
        
        # Step 3: Analyze target audience visual preferences
        audience_preferences = self._analyze_audience_visual_preferences()
        
        # Step 4: Create visual style recommendations
        style_recommendations = self._create_style_recommendations(
            personality_analysis, industry_standards, audience_preferences
        )
        
        # Step 5: Generate color psychology recommendations
        color_psychology = self._generate_color_psychology_recommendations()
        
        # Step 6: Create typography guidelines
        typography_guidelines = self._create_typography_guidelines()
        
        # Step 7: Define visual consistency standards
        consistency_standards = self._define_visual_consistency_standards()
        
        return {
            "brand_personality_analysis": personality_analysis,
            "industry_visual_standards": industry_standards,
            "audience_visual_preferences": audience_preferences,
            "style_recommendations": style_recommendations,
            "color_psychology": color_psychology,
            "typography_guidelines": typography_guidelines,
            "visual_consistency_standards": consistency_standards,
            "implementation_guidelines": self._create_implementation_guidelines()
        }

    def _analyze_personality_for_visuals(self) -> Dict[str, Any]:
        """Analyzes brand personality to determine visual characteristics"""
        
        voice = self.brand_personality["brand_voice"].lower()
        tone = self.brand_personality["brand_tone"].lower()
        values = self.brand_personality["core_values"].lower()
        adjectives = self.brand_personality.get("personality_adjectives", "").lower()
        
        # Determine visual personality type
        visual_personality = self._determine_visual_personality_type(voice, tone)
        
        # Analyze values for visual translation
        values_translation = self._translate_values_to_visual_characteristics(values)
        
        # Determine emotional tone for visuals
        emotional_tone = self._determine_visual_emotional_tone(tone)
        
        # Create personality-based design principles
        design_principles = self._create_personality_design_principles(
            visual_personality, emotional_tone, values_translation
        )
        
        return {
            "visual_personality_type": visual_personality,
            "emotional_tone": emotional_tone,
            "values_visual_translation": values_translation,
            "design_principles": design_principles,
            "personality_keywords": self._extract_personality_keywords(adjectives)
        }

    def _determine_visual_personality_type(self, voice: str, tone: str) -> str:
        """Determines the visual personality type based on brand voice and tone"""
        
        # Professional and authoritative
        if any(word in voice for word in ["professional", "authoritative", "expert", "formal"]):
            return "professional_authority"
        
        # Friendly and approachable
        elif any(word in voice for word in ["friendly", "approachable", "casual", "welcoming"]):
            return "friendly_approachable"
        
        # Innovative and cutting-edge
        elif any(word in voice for word in ["innovative", "cutting-edge", "modern", "forward-thinking"]):
            return "innovative_modern"
        
        # Playful and energetic
        elif any(word in voice for word in ["playful", "energetic", "fun", "dynamic"]):
            return "playful_energetic"
        
        # Trustworthy and reliable
        elif any(word in voice for word in ["trustworthy", "reliable", "consistent", "stable"]):
            return "trustworthy_reliable"
        
        else:
            return "balanced_versatile"

    def _translate_values_to_visual_characteristics(self, values: str) -> Dict[str, List[str]]:
        """Translates brand values into visual characteristics"""
        
        value_translations = {
            "innovation": {
                "visual_characteristics": ["Modern design elements", "Forward-thinking layouts", "Creative compositions"],
                "color_associations": ["Blue (trust)", "Purple (creativity)", "Silver (innovation)"],
                "typography_style": ["Modern sans-serif", "Clean lines", "Contemporary feel"]
            },
            "quality": {
                "visual_characteristics": ["High-resolution imagery", "Premium feel", "Attention to detail"],
                "color_associations": ["Gold (premium)", "Deep blue (reliability)", "White (purity)"],
                "typography_style": ["Refined fonts", "Elegant spacing", "Professional appearance"]
            },
            "trust": {
                "visual_characteristics": ["Professional photography", "Consistent branding", "Authentic imagery"],
                "color_associations": ["Blue (trust)", "Green (stability)", "Neutral tones"],
                "typography_style": ["Readable fonts", "Consistent hierarchy", "Professional styling"]
            },
            "customer-first": {
                "visual_characteristics": ["People-focused imagery", "Customer testimonials", "Service-oriented visuals"],
                "color_associations": ["Warm colors", "Approachable tones", "Inviting palette"],
                "typography_style": ["Friendly fonts", "Approachable styling", "Readable design"]
            },
            "transparency": {
                "visual_characteristics": ["Clean layouts", "Honest imagery", "Straightforward design"],
                "color_associations": ["Clear whites", "Honest blues", "Transparent elements"],
                "typography_style": ["Clear fonts", "Open spacing", "Honest presentation"]
            },
            "sustainability": {
                "visual_characteristics": ["Natural imagery", "Eco-friendly elements", "Organic shapes"],
                "color_associations": ["Green tones", "Natural colors", "Earth tones"],
                "typography_style": ["Organic fonts", "Natural feel", "Eco-conscious design"]
            }
        }
        
        # Find matching values
        matching_values = {}
        for value_key, translation in value_translations.items():
            if value_key in values.lower():
                matching_values[value_key] = translation
        
        return matching_values if matching_values else {
            "general": {
                "visual_characteristics": ["Professional appearance", "Consistent branding", "Quality imagery"],
                "color_associations": ["Brand colors", "Professional palette", "Consistent tones"],
                "typography_style": ["Readable fonts", "Professional styling", "Consistent hierarchy"]
            }
        }

    def _determine_visual_emotional_tone(self, tone: str) -> Dict[str, Any]:
        """Determines the emotional tone for visual design"""
        
        tone_mappings = {
            "encouraging": {
                "emotional_quality": "Uplifting and motivating",
                "visual_characteristics": ["Bright colors", "Positive imagery", "Inspiring compositions"],
                "mood": "Optimistic and forward-looking"
            },
            "supportive": {
                "emotional_quality": "Warm and caring",
                "visual_characteristics": ["Warm colors", "Approachable imagery", "Comforting layouts"],
                "mood": "Welcoming and supportive"
            },
            "confident": {
                "emotional_quality": "Strong and assured",
                "visual_characteristics": ["Bold colors", "Strong compositions", "Assertive imagery"],
                "mood": "Self-assured and powerful"
            },
            "professional": {
                "emotional_quality": "Competent and reliable",
                "visual_characteristics": ["Clean design", "Professional imagery", "Organized layouts"],
                "mood": "Trustworthy and capable"
            },
            "friendly": {
                "emotional_quality": "Approachable and warm",
                "visual_characteristics": ["Inviting colors", "Friendly imagery", "Welcoming layouts"],
                "mood": "Open and accessible"
            }
        }
        
        for tone_key, mapping in tone_mappings.items():
            if tone_key in tone.lower():
                return mapping
        
        # Default emotional tone
        return {
            "emotional_quality": "Balanced and versatile",
            "visual_characteristics": ["Neutral colors", "Professional imagery", "Clean layouts"],
            "mood": "Professional and approachable"
        }

    def _create_personality_design_principles(self, personality_type: str, emotional_tone: Dict, 
                                            values_translation: Dict) -> List[str]:
        """Creates design principles based on personality analysis"""
        
        personality_principles = {
            "professional_authority": [
                "Use clean, organized layouts with clear hierarchy",
                "Maintain consistent, professional typography",
                "Employ high-quality, business-appropriate imagery",
                "Use conservative color palettes with strategic accent colors"
            ],
            "friendly_approachable": [
                "Use rounded, soft design elements",
                "Incorporate warm, inviting color schemes",
                "Include people-focused imagery and testimonials",
                "Maintain open, welcoming layouts with generous white space"
            ],
            "innovative_modern": [
                "Embrace cutting-edge design trends and modern aesthetics",
                "Use bold, contemporary typography and layouts",
                "Incorporate dynamic visual elements and creative compositions",
                "Employ fresh, vibrant color palettes"
            ],
            "playful_energetic": [
                "Use dynamic, movement-oriented design elements",
                "Incorporate bright, energetic color schemes",
                "Include fun, engaging imagery and interactive elements",
                "Maintain lively, energetic layouts with visual interest"
            ],
            "trustworthy_reliable": [
                "Use stable, balanced compositions",
                "Employ consistent, reliable design patterns",
                "Incorporate authentic, credible imagery",
                "Maintain conservative, dependable color choices"
            ],
            "balanced_versatile": [
                "Create adaptable designs that work across contexts",
                "Use flexible, versatile design elements",
                "Maintain professional appearance with personality touches",
                "Employ balanced color palettes with strategic accents"
            ]
        }
        
        base_principles = personality_principles.get(personality_type, personality_principles["balanced_versatile"])
        
        # Add emotional tone principles
        emotional_principles = [
            f"Incorporate {emotional_tone['visual_characteristics'][0].lower()}",
            f"Maintain {emotional_tone['mood']} visual mood",
            f"Use {emotional_tone['emotional_quality'].lower()} design approach"
        ]
        
        return base_principles + emotional_principles

    def _extract_personality_keywords(self, adjectives: str) -> List[str]:
        """Extracts personality keywords from adjectives"""
        
        if not adjectives:
            return ["professional", "reliable"]
        
        # Split and clean adjectives
        keyword_list = [adj.strip() for adj in adjectives.split(",") if adj.strip()]
        
        # Add visual synonyms for common personality traits
        visual_synonyms = {
            "trustworthy": ["reliable", "dependable", "credible"],
            "innovative": ["creative", "forward-thinking", "modern"],
            "friendly": ["approachable", "welcoming", "warm"],
            "professional": ["polished", "refined", "sophisticated"],
            "energetic": ["dynamic", "vibrant", "lively"]
        }
        
        expanded_keywords = []
        for keyword in keyword_list:
            expanded_keywords.append(keyword)
            if keyword in visual_synonyms:
                expanded_keywords.extend(visual_synonyms[keyword][:2])  # Add top 2 synonyms
        
        return expanded_keywords[:10]  # Limit to 10 keywords

    def _determine_industry_visual_standards(self) -> Dict[str, Any]:
        """Determines industry-appropriate visual standards"""
        
        industry_standards = {
            "technology": {
                "visual_style": "Modern, clean, tech-forward",
                "color_preferences": ["Blue", "White", "Gray", "Accent colors"],
                "typography_style": "Clean sans-serif, modern fonts",
                "imagery_style": "High-tech, innovative, professional",
                "design_trends": ["Minimalism", "Flat design", "Clean layouts"],
                "avoid": ["Outdated design patterns", "Overly decorative elements"]
            },
            "healthcare": {
                "visual_style": "Clean, trustworthy, professional",
                "color_preferences": ["Blue", "White", "Green", "Soft tones"],
                "typography_style": "Readable, professional fonts",
                "imagery_style": "Professional, caring, trustworthy",
                "design_trends": ["Clean layouts", "Professional photography", "Trust-building design"],
                "avoid": ["Overly flashy designs", "Unprofessional imagery"]
            },
            "e-commerce": {
                "visual_style": "Product-focused, conversion-optimized",
                "color_preferences": ["Brand colors", "High contrast", "Call-to-action colors"],
                "typography_style": "Clear, readable, conversion-focused",
                "imagery_style": "High-quality product photos, lifestyle imagery",
                "design_trends": ["Product showcases", "Social proof", "Clear CTAs"],
                "avoid": ["Cluttered layouts", "Poor product photography"]
            },
            "professional_services": {
                "visual_style": "Professional, authoritative, trustworthy",
                "color_preferences": ["Blue", "Gray", "Professional tones"],
                "typography_style": "Professional, readable fonts",
                "imagery_style": "Professional, business-appropriate",
                "design_trends": ["Clean layouts", "Professional imagery", "Trust-building elements"],
                "avoid": ["Casual design elements", "Unprofessional imagery"]
            }
        }
        
        # Find matching industry
        industry_key = self.industry.lower()
        for key in industry_standards.keys():
            if key in industry_key:
                return industry_standards[key]
        
        # Default to professional services if no match
        return industry_standards["professional_services"]

    def _analyze_audience_visual_preferences(self) -> Dict[str, Any]:
        """Analyzes target audience visual preferences"""
        
        audience_lower = self.target_audience.lower()
        
        # Determine audience demographics
        age_group = self._determine_age_group(audience_lower)
        audience_type = self._determine_audience_type(audience_lower)
        
        # Get preferences based on demographics
        age_preferences = self._get_age_based_preferences(age_group)
        type_preferences = self._get_type_based_preferences(audience_type)
        
        return {
            "age_group": age_group,
            "audience_type": audience_type,
            "visual_preferences": age_preferences,
            "content_preferences": type_preferences,
            "design_considerations": self._create_audience_design_considerations(age_group, audience_type)
        }

    def _determine_age_group(self, audience_text: str) -> str:
        """Determines age group from audience description"""
        
        if any(term in audience_text for term in ["18-25", "gen z", "young", "student"]):
            return "Gen Z"
        elif any(term in audience_text for term in ["25-40", "millennial", "young professional"]):
            return "Millennial"
        elif any(term in audience_text for term in ["40-60", "gen x", "mature", "established"]):
            return "Gen X"
        elif any(term in audience_text for term in ["60+", "baby boomer", "senior"]):
            return "Baby Boomer"
        else:
            return "Mixed"

    def _determine_audience_type(self, audience_text: str) -> str:
        """Determines audience type from description"""
        
        if any(term in audience_text for term in ["business", "professional", "executive", "corporate"]):
            return "Business Professional"
        elif any(term in audience_text for term in ["consumer", "customer", "shopper", "buyer"]):
            return "Consumer"
        elif any(term in audience_text for term in ["student", "learner", "education", "academic"]):
            return "Student/Educational"
        elif any(term in audience_text for term in ["entrepreneur", "startup", "small business"]):
            return "Entrepreneur"
        else:
            return "General"

    def _get_age_based_preferences(self, age_group: str) -> Dict[str, List[str]]:
        """Gets visual preferences based on age group"""
        
        preferences = {
            "Gen Z": {
                "visual_style": ["Bold", "Vibrant", "Authentic", "Social media native"],
                "color_preferences": ["Bright colors", "High contrast", "Trending palettes"],
                "content_types": ["Short-form video", "Interactive content", "User-generated content"],
                "design_elements": ["Dynamic layouts", "Bold typography", "Authentic imagery"]
            },
            "Millennial": {
                "visual_style": ["Modern", "Clean", "Balanced", "Mobile-optimized"],
                "color_preferences": ["Balanced palettes", "Brand colors", "Professional tones"],
                "content_types": ["Visual content", "Educational content", "Behind-the-scenes"],
                "design_elements": ["Clean layouts", "Professional imagery", "Readable typography"]
            },
            "Gen X": {
                "visual_style": ["Professional", "Trustworthy", "Clear", "Detailed"],
                "color_preferences": ["Conservative colors", "Professional tones", "Subtle accents"],
                "content_types": ["Educational content", "Professional insights", "Detailed information"],
                "design_elements": ["Clear layouts", "Professional photography", "Readable fonts"]
            },
            "Baby Boomer": {
                "visual_style": ["Traditional", "Clear", "Readable", "Professional"],
                "color_preferences": ["Conservative palettes", "High contrast", "Readable colors"],
                "content_types": ["Detailed content", "Professional information", "Traditional formats"],
                "design_elements": ["Large fonts", "Clear layouts", "Traditional imagery"]
            },
            "Mixed": {
                "visual_style": ["Versatile", "Accessible", "Professional", "Inclusive"],
                "color_preferences": ["Balanced palettes", "Accessible colors", "Professional tones"],
                "content_types": ["Varied content types", "Accessible formats", "Multi-generational appeal"],
                "design_elements": ["Flexible layouts", "Readable fonts", "Inclusive imagery"]
            }
        }
        
        return preferences.get(age_group, preferences["Mixed"])

    def _get_type_based_preferences(self, audience_type: str) -> Dict[str, List[str]]:
        """Gets preferences based on audience type"""
        
        preferences = {
            "Business Professional": {
                "content_focus": ["Industry insights", "Professional development", "Business solutions"],
                "visual_approach": ["Professional imagery", "Clean layouts", "Business-appropriate design"],
                "engagement_preferences": ["Thought leadership", "Expert content", "Professional networking"]
            },
            "Consumer": {
                "content_focus": ["Product benefits", "Lifestyle content", "Customer stories"],
                "visual_approach": ["Lifestyle imagery", "Product showcases", "Relatable content"],
                "engagement_preferences": ["User-generated content", "Reviews", "Social proof"]
            },
            "Student/Educational": {
                "content_focus": ["Educational content", "How-to guides", "Learning resources"],
                "visual_approach": ["Clear, educational layouts", "Step-by-step visuals", "Informative design"],
                "engagement_preferences": ["Interactive content", "Learning materials", "Educational resources"]
            },
            "Entrepreneur": {
                "content_focus": ["Business tips", "Success stories", "Industry insights"],
                "visual_approach": ["Motivational imagery", "Success-focused design", "Professional presentation"],
                "engagement_preferences": ["Business advice", "Success stories", "Networking opportunities"]
            },
            "General": {
                "content_focus": ["Broad appeal content", "General information", "Varied topics"],
                "visual_approach": ["Versatile design", "Inclusive imagery", "Accessible layouts"],
                "engagement_preferences": ["General engagement", "Broad appeal", "Inclusive content"]
            }
        }
        
        return preferences.get(audience_type, preferences["General"])

    def _create_audience_design_considerations(self, age_group: str, audience_type: str) -> List[str]:
        """Creates design considerations based on audience analysis"""
        
        considerations = []
        
        # Age-based considerations
        if age_group == "Gen Z":
            considerations.extend([
                "Design for mobile-first experience",
                "Use bold, attention-grabbing visuals",
                "Incorporate social media native elements",
                "Ensure fast loading and snappy interactions"
            ])
        elif age_group == "Millennial":
            considerations.extend([
                "Balance professional and approachable design",
                "Optimize for mobile and desktop viewing",
                "Use modern, clean aesthetic",
                "Ensure easy sharing and engagement"
            ])
        elif age_group in ["Gen X", "Baby Boomer"]:
            considerations.extend([
                "Prioritize readability and clarity",
                "Use larger fonts and clear layouts",
                "Maintain professional appearance",
                "Ensure accessibility and usability"
            ])
        
        # Type-based considerations
        if audience_type == "Business Professional":
            considerations.extend([
                "Maintain professional credibility",
                "Use business-appropriate imagery",
                "Ensure information hierarchy is clear",
                "Focus on thought leadership presentation"
            ])
        elif audience_type == "Consumer":
            considerations.extend([
                "Create emotional connection",
                "Use lifestyle and aspirational imagery",
                "Focus on benefits and outcomes",
                "Ensure easy decision-making support"
            ])
        
        return considerations

    def _create_style_recommendations(self, personality_analysis: Dict, industry_standards: Dict, 
                                    audience_preferences: Dict) -> Dict[str, Any]:
        """Creates comprehensive style recommendations"""
        
        # Combine personality and industry standards
        combined_style = self._combine_personality_and_industry_style(
            personality_analysis, industry_standards
        )
        
        # Adjust for audience preferences
        audience_adjusted_style = self._adjust_style_for_audience(
            combined_style, audience_preferences
        )
        
        return {
            "overall_style_direction": audience_adjusted_style,
            "key_style_elements": self._define_key_style_elements(combined_style),
            "style_consistency_guidelines": self._create_consistency_guidelines(),
            "style_evolution_recommendations": self._suggest_style_evolution()
        }

    def _combine_personality_and_industry_style(self, personality: Dict, industry: Dict) -> Dict[str, Any]:
        """Combines personality and industry style recommendations"""
        
        return {
            "visual_approach": f"{personality['visual_personality_type']} meets {industry['visual_style']}",
            "color_strategy": f"Industry-appropriate colors with {personality['emotional_tone']['emotional_quality']} emphasis",
            "typography_approach": f"{industry['typography_style']} with {personality['design_principles'][0].lower()}",
            "imagery_style": f"{industry['imagery_style']} reflecting {personality['emotional_tone']['mood']}",
            "design_philosophy": f"Balancing {industry['visual_style']} industry standards with {personality['visual_personality_type']} brand personality"
        }

    def _adjust_style_for_audience(self, combined_style: Dict, audience_preferences: Dict) -> str:
        """Adjusts style recommendations for audience preferences"""
        
        age_preferences = audience_preferences.get("visual_preferences", {})
        type_preferences = audience_preferences.get("content_preferences", {})
        
        # Create audience-adjusted style description
        style_elements = []
        
        if age_preferences.get("visual_style"):
            style_elements.append(f"age-appropriate {age_preferences['visual_style'][0].lower()} styling")
        
        if type_preferences.get("visual_approach"):
            style_elements.append(f"{type_preferences['visual_approach'][0].lower()} approach")
        
        audience_adjustment = f"Audience-optimized: {', '.join(style_elements)}" if style_elements else "General audience appeal"
        
        return f"{combined_style['design_philosophy']} with {audience_adjustment}"

    def _define_key_style_elements(self, combined_style: Dict) -> List[Dict[str, str]]:
        """Defines key style elements for implementation"""
        
        return [
            {
                "element": "Color Palette",
                "description": combined_style["color_strategy"],
                "implementation": "Use industry colors with personality-driven accents"
            },
            {
                "element": "Typography",
                "description": combined_style["typography_approach"],
                "implementation": "Maintain readability while reflecting brand personality"
            },
            {
                "element": "Imagery Style",
                "description": combined_style["imagery_style"],
                "implementation": "Source imagery that reflects both industry standards and brand mood"
            },
            {
                "element": "Layout Approach",
                "description": combined_style["visual_approach"],
                "implementation": "Balance professional standards with personality expression"
            }
        ]

    def _create_consistency_guidelines(self) -> List[str]:
        """Creates guidelines for maintaining style consistency"""
        
        return [
            "Maintain consistent color palette across all materials",
            "Use consistent typography hierarchy and font choices",
            "Apply consistent spacing and layout principles",
            "Ensure imagery style consistency across all content",
            "Maintain brand personality expression in all visual elements",
            "Regularly audit visual materials for consistency compliance"
        ]

    def _suggest_style_evolution(self) -> Dict[str, Any]:
        """Suggests how the visual style might evolve over time"""
        
        return {
            "short_term_evolution": [
                "Refine color palette based on performance data",
                "Optimize typography for better readability",
                "Improve imagery selection based on engagement metrics"
            ],
            "long_term_evolution": [
                "Gradually modernize design elements while maintaining brand recognition",
                "Incorporate new design trends that align with brand personality",
                "Evolve visual style to match brand growth and market position"
            ],
            "evolution_principles": [
                "Maintain brand recognition throughout changes",
                "Test changes with target audience before full implementation",
                "Document all style changes for consistency",
                "Ensure evolution aligns with brand values and personality"
            ]
        }

    def _generate_color_psychology_recommendations(self) -> Dict[str, Any]:
        """Generates color psychology recommendations based on brand analysis"""
        
        voice = self.brand_personality["brand_voice"].lower()
        tone = self.brand_personality["brand_tone"].lower()
        industry = self.industry.lower()
        
        # Determine primary color psychology needs
        if "professional" in voice or "formal" in voice:
            primary_color_psychology = "Trust, reliability, professionalism"
            recommended_colors = ["Blue", "Gray", "White"]
        elif "friendly" in voice or "casual" in voice:
            primary_color_psychology = "Approachability, warmth, friendliness"
            recommended_colors = ["Orange", "Yellow", "Green"]
        elif "innovative" in voice or "modern" in voice:
            primary_color_psychology = "Innovation, creativity, forward-thinking"
            recommended_colors = ["Purple", "Blue", "Silver"]
        else:
            primary_color_psychology = "Balance, versatility, professionalism"
            recommended_colors = ["Blue", "Gray", "Accent colors"]
        
        # Add industry-specific color considerations
        industry_color_adjustments = {
            "healthcare": ["Blue (trust)", "Green (health)", "White (cleanliness)"],
            "technology": ["Blue (trust)", "Gray (professional)", "Accent colors (innovation)"],
            "finance": ["Blue (trust)", "Green (money)", "Gray (stability)"],
            "e-commerce": ["Brand colors", "High contrast", "CTA colors"]
        }
        
        industry_colors = []
        for key, colors in industry_color_adjustments.items():
            if key in industry:
                industry_colors = colors
                break
        
        return {
            "primary_color_psychology": primary_color_psychology,
            "recommended_colors": recommended_colors,
            "industry_color_considerations": industry_colors,
            "color_combination_strategy": self._create_color_combination_strategy(),
            "accessibility_considerations": [
                "Ensure sufficient contrast ratios (WCAG AA standards)",
                "Test color combinations for colorblind accessibility",
                "Provide alternative text for color-dependent information"
            ]
        }

    def _create_color_combination_strategy(self) -> str:
        """Creates color combination strategy"""
        
        return (
            "Use 60-30-10 rule: 60% primary brand color, 30% secondary color, "
            "10% accent color. Maintain consistent color hierarchy across all materials."
        )

    def _create_typography_guidelines(self) -> Dict[str, Any]:
        """Creates comprehensive typography guidelines"""
        
        voice = self.brand_personality["brand_voice"].lower()
        
        # Determine typography personality
        if "professional" in voice or "formal" in voice:
            typography_personality = "Professional and authoritative"
            font_characteristics = ["Clean sans-serif fonts", "High readability", "Conservative styling"]
        elif "friendly" in voice or "casual" in voice:
            typography_personality = "Approachable and friendly"
            font_characteristics = ["Rounded fonts", "Warm feel", "Inviting typography"]
        elif "innovative" in voice or "modern" in voice:
            typography_personality = "Modern and innovative"
            font_characteristics = ["Contemporary fonts", "Bold styling", "Forward-thinking design"]
        else:
            typography_personality = "Balanced and versatile"
            font_characteristics = ["Readable fonts", "Professional with personality", "Flexible styling"]
        
        return {
            "typography_personality": typography_personality,
            "font_characteristics": font_characteristics,
            "hierarchy_guidelines": [
                "Use maximum 3 font sizes for hierarchy",
                "Maintain consistent font weights throughout",
                "Ensure sufficient contrast between text and background",
                "Use appropriate line spacing for readability"
            ],
            "font_selection_criteria": [
                "Readability at all sizes",
                "Consistency with brand personality",
                "Availability across platforms",
                "Professional appearance"
            ],
            "implementation_standards": [
                "Define font sizes for headings, subheadings, and body text",
                "Establish consistent spacing between elements",
                "Create font usage guidelines for different contexts",
                "Ensure accessibility compliance"
            ]
        }

    def _define_visual_consistency_standards(self) -> Dict[str, Any]:
        """Defines standards for maintaining visual consistency"""
        
        return {
            "brand_identity_elements": [
                "Logo usage and placement",
                "Color palette application",
                "Typography consistency",
                "Imagery style standards"
            ],
            "consistency_checkpoints": [
                "All materials use approved color palette",
                "Typography follows established hierarchy",
                "Imagery reflects brand personality",
                "Layout follows brand design principles"
            ],
            "quality_standards": [
                "High-resolution imagery only",
                "Consistent spacing and alignment",
                "Professional appearance across all materials",
                "Accessibility compliance maintained"
            ],
            "documentation_requirements": [
                "Style guide maintenance",
                "Asset library organization",
                "Usage guidelines documentation",
                "Regular consistency audits"
            ]
        }

    def _create_implementation_guidelines(self) -> Dict[str, Any]:
        """Creates guidelines for implementing the visual analysis"""
        
        return {
            "immediate_actions": [
                "Create comprehensive style guide based on analysis",
                "Establish color palette and typography standards",
                "Define imagery selection criteria",
                "Set up asset management system"
            ],
            "ongoing_processes": [
                "Regular style guide updates and maintenance",
                "Consistent application across all materials",
                "Performance monitoring and optimization",
                "Team training on brand visual standards"
            ],
            "success_metrics": [
                "Consistent brand recognition across touchpoints",
                "Improved engagement with cohesive visual identity",
                "Professional appearance that builds trust",
                "Alignment between visual identity and brand personality"
            ],
            "tools_and_resources": [
                "Brand style guide document",
                "Color palette specifications",
                "Typography guidelines",
                "Imagery selection criteria",
                "Design templates and assets"
            ]
        }

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = BrandVisualAnalyzer(
        brand_personality={
            "brand_voice": "Professional and authoritative",
            "brand_tone": "Encouraging and supportive",
            "core_values": "Innovation, quality, customer-first",
            "personality_adjectives": "trustworthy, innovative, reliable"
        },
        industry="Technology",
        target_audience="Small business owners aged 25-45"
    )
    print(tool.run())
