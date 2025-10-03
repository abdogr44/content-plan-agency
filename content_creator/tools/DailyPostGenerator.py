from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from typing import Dict, Any

class DailyPostGenerator(BaseTool):
    """
    Creates detailed content for each day of the week including goals, types, titles, and captions
    based on strategic framework and brand voice.
    """
    
    day_number: int = Field(
        ..., description="Day of the week (1-7, where 1=Monday, 2=Tuesday, etc.)"
    )
    content_theme: str = Field(
        ..., description="Strategic theme for the day (e.g., 'Educational Content', 'Behind-the-Scenes', 'Problem-Solution')"
    )
    post_type: str = Field(
        ..., description="Recommended post type from strategy (e.g., 'Image Post', 'Video', 'Story', 'Article')"
    )
    target_audience: str = Field(
        ..., description="Audience characteristics for content personalization"
    )
    brand_voice: str = Field(
        ..., description="Brand communication style and voice"
    )
    platform: str = Field(
        ..., description="Target platform for the post (Facebook, Instagram, LinkedIn)"
    )

    def run(self):
        """
        Generates complete post details for a specific day including title, caption, and goal.
        """
        # Step 1: Validate inputs
        if not (1 <= self.day_number <= 7):
            return "Error: Day number must be between 1 and 7."
        
        # Step 2: Get additional context from agency context
        business_data = self._context.get("business_data")
        brand_personality = self._context.get("brand_personality")
        strategy_framework = self._context.get("strategy_framework")
        
        if not all([business_data, brand_personality, strategy_framework]):
            return "Error: Missing required context data. Please ensure strategy analysis is completed first."
        
        # Step 3: Generate post content
        post_content = self._generate_post_content(
            business_data, brand_personality, strategy_framework
        )
        
        # Step 4: Store individual post in context
        post_key = f"day_{self.day_number}_post"
        self._context.set(post_key, post_content)
        
        # Step 5: Return generated post content
        return json.dumps({
            "status": "success",
            "message": f"Post generated successfully for Day {self.day_number}",
            "post_content": post_content
        }, indent=2)

    def _generate_post_content(self, business_data: Dict, brand_personality: Dict, 
                             strategy_framework: Dict) -> Dict[str, Any]:
        """Generates comprehensive post content based on strategic framework"""
        
        # Step 1: Determine optimal goal for the day
        goal = self._determine_post_goal(self.day_number, self.content_theme, 
                                       strategy_framework["content_strategy"]["weekly_structure"])
        
        # Step 2: Generate platform-optimized title
        title = self._generate_title(self.content_theme, self.target_audience, 
                                   brand_personality["brand_voice"], self.platform)
        
        # Step 3: Create engaging caption
        caption = self._generate_caption(self.content_theme, self.post_type, 
                                       business_data, brand_personality, self.platform)
        
        # Step 4: Optimize content for platform
        platform_optimization = self._optimize_for_platform(self.platform, self.post_type)
        
        return {
            "day": self.day_number,
            "day_name": self._get_day_name(self.day_number),
            "platform": self.platform,
            "goal": goal,
            "type_of_post": self.post_type,
            "title": title,
            "caption": caption,
            "content_theme": self.content_theme,
            "platform_optimization": platform_optimization,
            "brand_alignment": {
                "voice": brand_personality["brand_voice"],
                "tone": brand_personality["brand_tone"],
                "values": brand_personality["core_values"]
            },
            "target_audience": self.target_audience,
            "generation_timestamp": self._get_current_timestamp()
        }

    def _determine_post_goal(self, day_number: int, theme: str, weekly_structure: Dict) -> str:
        """Determines the primary goal for the post based on day and theme"""
        
        # Get focus areas from weekly structure
        day_name = self._get_day_name(day_number)
        day_focus = weekly_structure.get(day_name, {}).get("focus_areas", "engagement")
        
        # Map focus areas to specific goals
        goal_mapping = {
            "engagement": "Increase audience engagement and interaction",
            "education": "Educate audience about industry topics and solutions",
            "brand_awareness": "Build brand visibility and recognition",
            "lead_generation": "Generate qualified leads and prospects",
            "conversion": "Drive sales and conversions"
        }
        
        # Theme-specific goal adjustments
        if "Educational" in theme:
            return "Educate audience about industry topics and establish thought leadership"
        elif "Behind-the-Scenes" in theme:
            return "Build trust and humanize the brand through authentic content"
        elif "Problem-Solution" in theme:
            return "Address customer pain points and showcase solution value"
        else:
            return goal_mapping.get(day_focus, "Increase audience engagement and interaction")

    def _generate_title(self, theme: str, audience: str, voice: str, platform: str) -> str:
        """Generates compelling title based on theme, audience, and brand voice"""
        
        # Platform-specific title optimization
        if platform == "LinkedIn":
            # Professional and informative titles work best
            title_templates = [
                f"How [Industry] Professionals Can {self._get_action_from_theme(theme)}",
                f"The {self._get_adjective_from_voice(voice)} Guide to {theme}",
                f"Why {audience.split(',')[0]} Need to Know About {theme}"
            ]
        elif platform == "Instagram":
            # Engaging and visual titles
            title_templates = [
                f"✨ {theme}: What You Need to Know",
                f"Behind the Scenes: {theme} Edition",
                f"The {self._get_adjective_from_voice(voice)} Way to {theme}"
            ]
        else:  # Facebook
            # Conversational and community-focused
            title_templates = [
                f"Let's Talk About {theme}",
                f"Your {theme} Questions Answered",
                f"The Truth About {theme} for {audience.split(',')[0]}"
            ]
        
        # Select and customize template
        import random
        selected_template = random.choice(title_templates)
        
        # Replace placeholders with actual content
        title = selected_template.replace("[Industry]", "Your Industry")
        
        return title

    def _generate_caption(self, theme: str, post_type: str, business_data: Dict, 
                         brand_personality: Dict, platform: str) -> str:
        """Generates engaging caption that reflects brand voice and encourages engagement"""
        
        # Base caption structure
        caption_parts = []
        
        # Opening hook based on theme
        hook = self._create_engaging_hook(theme, brand_personality["brand_voice"])
        caption_parts.append(hook)
        
        # Main content based on theme
        main_content = self._create_main_content(theme, business_data, brand_personality)
        caption_parts.append(main_content)
        
        # Call-to-action
        cta = self._create_call_to_action(platform, brand_personality["brand_tone"])
        caption_parts.append(cta)
        
        # Platform-specific formatting
        caption = self._format_caption_for_platform("\n\n".join(caption_parts), platform)
        
        return caption

    def _create_engaging_hook(self, theme: str, voice: str) -> str:
        """Creates an engaging opening hook for the caption"""
        hooks = {
            "Educational Content": [
                "Did you know that...",
                "Here's something most people don't realize...",
                "Quick question for you..."
            ],
            "Behind-the-Scenes": [
                "Ever wondered what goes on behind the scenes?",
                "Today we're pulling back the curtain...",
                "Here's what a typical day looks like..."
            ],
            "Problem-Solution": [
                "Struggling with [problem]? You're not alone.",
                "We hear this challenge all the time...",
                "If you're dealing with [problem], this is for you."
            ]
        }
        
        import random
        available_hooks = hooks.get(theme, hooks["Educational Content"])
        return random.choice(available_hooks)

    def _create_main_content(self, theme: str, business_data: Dict, brand_personality: Dict) -> str:
        """Creates the main content body for the caption"""
        
        if theme == "Educational Content":
            return f"As {business_data['industry']} professionals, it's crucial to stay informed about industry trends and best practices. Here are three key insights that can help {business_data['target_audience']} stay ahead of the curve."
        
        elif theme == "Behind-the-Scenes":
            return f"At our company, we believe in {brand_personality['core_values']}. Today, we're sharing a glimpse into our process and the people who make it all possible."
        
        elif theme == "Problem-Solution":
            return f"We understand that {business_data['current_challenges']} can be challenging. That's why we've developed solutions specifically designed for {business_data['target_audience']}."
        
        else:
            return f"Our approach is rooted in {brand_personality['core_values']}, ensuring we deliver value to {business_data['target_audience']}."

    def _create_call_to_action(self, platform: str, tone: str) -> str:
        """Creates platform-appropriate call-to-action"""
        
        if platform == "LinkedIn":
            ctas = [
                "What are your thoughts on this? Share your experience in the comments below.",
                "Have you faced similar challenges? Let's discuss in the comments.",
                "I'd love to hear your perspective on this topic."
            ]
        elif platform == "Instagram":
            ctas = [
                "Double tap if you agree! 👆",
                "What's your take on this? Let us know below! 👇",
                "Tag someone who needs to see this! 👥"
            ]
        else:  # Facebook
            ctas = [
                "What do you think? Share your thoughts below!",
                "Have you experienced this? Tell us your story!",
                "We'd love to hear from you - comment below!"
            ]
        
        import random
        return random.choice(ctas)

    def _format_caption_for_platform(self, caption: str, platform: str) -> str:
        """Formats caption for optimal platform performance"""
        
        if platform == "Instagram":
            # Add line breaks for readability
            return caption.replace(". ", ".\n\n")
        elif platform == "LinkedIn":
            # Keep professional formatting
            return caption
        else:  # Facebook
            # Balance between casual and professional
            return caption

    def _optimize_for_platform(self, platform: str, post_type: str) -> Dict[str, Any]:
        """Provides platform-specific optimization recommendations"""
        
        optimizations = {
            "Facebook": {
                "best_posting_times": "9 AM - 3 PM",
                "optimal_length": "40-80 characters for titles",
                "engagement_tips": "Ask questions, share relatable content",
                "visual_recommendations": "High-quality images, 1200x630px for link previews"
            },
            "Instagram": {
                "best_posting_times": "11 AM - 1 PM, 5 PM - 7 PM",
                "optimal_length": "125 characters for captions",
                "engagement_tips": "Use Stories, engage with comments quickly",
                "visual_recommendations": "Square images 1080x1080px, high contrast"
            },
            "LinkedIn": {
                "best_posting_times": "8 AM - 10 AM, 12 PM - 2 PM",
                "optimal_length": "150-300 characters for optimal engagement",
                "engagement_tips": "Share professional insights, comment thoughtfully",
                "visual_recommendations": "Professional images, 1200x627px for articles"
            }
        }
        
        return optimizations.get(platform, {})

    def _get_action_from_theme(self, theme: str) -> str:
        """Extracts action verb from theme for title generation"""
        actions = {
            "Educational Content": "Stay Informed",
            "Behind-the-Scenes": "See the Process",
            "Problem-Solution": "Solve Problems"
        }
        return actions.get(theme, "Stay Ahead")

    def _get_adjective_from_voice(self, voice: str) -> str:
        """Extracts adjective from brand voice for title generation"""
        if "professional" in voice.lower():
            return "Professional"
        elif "casual" in voice.lower():
            return "Casual"
        elif "playful" in voice.lower():
            return "Playful"
        else:
            return "Effective"

    def _get_day_name(self, day_number: int) -> str:
        """Converts day number to day name"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[day_number - 1]

    def _get_current_timestamp(self):
        """Helper method to get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()

if __name__ == "__main__":
    tool = DailyPostGenerator(
        day_number=1,
        content_theme="Educational Content",
        post_type="Image Post",
        target_audience="Small business owners aged 25-45",
        brand_voice="Professional and authoritative",
        platform="Instagram"
    )
    print(tool.run())
