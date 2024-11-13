from django.db import migrations


def add_fake_articles(apps, schema_editor):
    Article = apps.get_model("The_SQL_Heist_App", "Article")
    articles = [
        Article(
            title="Breaking News: Market Crash",
            content="The stock market experienced a significant crash today, with major indices falling by over 3%.",
        ),
        Article(
            title="Sports Update: Local Team Wins Championship",
            content="The local football team won the championship in a thrilling match that ended in a penalty shootout.",
        ),
        Article(
            title="Weather Alert: Heavy Rain Expected",
            content="Meteorologists are predicting heavy rain in the region over the next few days. Residents are advised to take precautions.",
        ),
        Article(
            title="Tech News: New Smartphone Released",
            content="A major tech company has released its latest smartphone model, featuring cutting-edge technology and a sleek design.",
        ),
        Article(
            title="Health Tips: How to Stay Fit",
            content="Experts share tips on how to maintain a healthy lifestyle through regular exercise and a balanced diet.",
        ),
        Article(
            title="Travel Guide: Top Destinations for 2023",
            content="Discover the top travel destinations for 2023, from exotic beaches to bustling cities.",
        ),
        Article(
            title="Entertainment: Upcoming Movie Releases",
            content="Check out the list of upcoming movie releases, including highly anticipated blockbusters and indie films.",
        ),
        Article(
            title="Finance: Tips for Saving Money",
            content="Financial advisors share their top tips for saving money and managing your finances effectively.",
        ),
        Article(
            title="Science: New Species Discovered",
            content="Scientists have discovered a new species of insect in the Amazon rainforest.",
        ),
        Article(
            title="Politics: Election Results Announced",
            content="The results of the recent election have been announced, with the incumbent party securing a majority.",
        ),
        Article(
            title="Economy: Inflation Rates Rise",
            content="Inflation rates have risen to their highest levels in a decade, impacting the cost of living.",
        ),
        Article(
            title="Education: New Curriculum Introduced",
            content="A new curriculum has been introduced in schools, focusing on STEM education.",
        ),
        Article(
            title="Environment: Conservation Efforts",
            content="Conservationists are working to protect endangered species through various initiatives.",
        ),
        Article(
            title="History: Ancient Artifacts Found",
            content="Archaeologists have uncovered ancient artifacts in a newly discovered site.",
        ),
        Article(
            title="Fashion: Latest Trends",
            content="The latest fashion trends for the season include bold colors and sustainable materials.",
        ),
        Article(
            title="Music: Concert Tour Announced",
            content="A popular band has announced their upcoming concert tour dates.",
        ),
        Article(
            title="Literature: Bestselling Books",
            content="Check out the list of bestselling books this month, featuring a mix of fiction and non-fiction.",
        ),
        Article(
            title="Automotive: New Car Models",
            content="Automakers have unveiled their new car models for the year, featuring advanced technology.",
        ),
        Article(
            title="Real Estate: Housing Market Trends",
            content="The housing market is experiencing significant changes, with prices fluctuating in various regions.",
        ),
        Article(
            title="Food: Gourmet Recipes",
            content="Discover gourmet recipes from top chefs that you can try at home.",
        ),
        Article(
            title="Travel: Budget-Friendly Tips",
            content="Learn how to travel on a budget with these tips and tricks.",
        ),
        Article(
            title="Fitness: Home Workout Routines",
            content="Stay fit with these home workout routines that require minimal equipment.",
        ),
        Article(
            title="Gaming: Upcoming Releases",
            content="Check out the list of upcoming video game releases, including highly anticipated titles.",
        ),
        Article(
            title="Art: Gallery Exhibitions",
            content="Explore the latest gallery exhibitions featuring contemporary and classic art.",
        ),
        Article(
            title="Theater: New Plays",
            content="Discover new plays that are being performed in theaters around the world.",
        ),
        Article(
            title="Photography: Tips for Beginners",
            content="Learn photography tips for beginners to help you capture stunning images.",
        ),
        Article(
            title="Gardening: Seasonal Plants",
            content="Find out which plants are best to grow in your garden this season.",
        ),
        Article(
            title="DIY: Home Improvement Projects",
            content="Get inspired with these DIY home improvement projects.",
        ),
        Article(
            title="Pets: Care Tips",
            content="Learn how to take care of your pets with these expert tips.",
        ),
        Article(
            title="Relationships: Advice from Experts",
            content="Relationship experts share their advice on maintaining healthy relationships.",
        ),
        Article(
            title="Career: Job Search Strategies",
            content="Discover effective job search strategies to help you land your dream job.",
        ),
        Article(
            title="Finance: Investment Opportunities",
            content="Explore various investment opportunities to grow your wealth.",
        ),
        Article(
            title="Science: Space Exploration",
            content="Read about the latest advancements in space exploration and upcoming missions.",
        ),
        Article(
            title="Health: Mental Wellness",
            content="Experts discuss the importance of mental wellness and how to achieve it.",
        ),
        Article(
            title="Technology: AI Innovations",
            content="Learn about the latest innovations in artificial intelligence and their applications.",
        ),
        Article(
            title="Culture: Festivals Around the World",
            content="Discover cultural festivals around the world that you can attend.",
        ),
        Article(
            title="Business: Startup Success Stories",
            content="Read about successful startups and the entrepreneurs behind them.",
        ),
        Article(
            title="Lifestyle: Minimalist Living",
            content="Explore the benefits of minimalist living and how to adopt this lifestyle.",
        ),
        Article(
            title="Education: Online Learning",
            content="The rise of online learning platforms has transformed education, making it more accessible to people worldwide.",
        ),
        Article(
            title="Health: Nutrition Tips",
            content="Nutritionists share their top tips for maintaining a balanced diet and healthy eating habits.",
        ),
        Article(
            title="Finance: Cryptocurrency Trends",
            content="Stay updated on the latest trends in cryptocurrency and blockchain technology.",
        ),
        Article(
            title="Travel: Adventure Destinations",
            content="Explore the best adventure travel destinations for thrill-seekers and outdoor enthusiasts.",
        ),
        Article(
            title="Technology: Cybersecurity",
            content="Learn about the latest developments in cybersecurity and how to protect your digital assets.",
        ),
        Article(
            title="Environment: Renewable Energy",
            content="Discover the advancements in renewable energy sources and their impact on the environment.",
        ),
        Article(
            title="Science: Medical Breakthroughs",
            content="Read about the latest medical breakthroughs and their potential to change healthcare.",
        ),
        Article(
            title="Fashion: Sustainable Brands",
            content="Check out sustainable fashion brands that are making a positive impact on the environment.",
        ),
        Article(
            title="Automotive: Electric Vehicles",
            content="Learn about the latest electric vehicles and their benefits over traditional cars.",
        ),
        Article(
            title="Food: Vegan Recipes",
            content="Try out these delicious vegan recipes that are both healthy and easy to make.",
        ),
        Article(
            title="Fitness: Yoga Practices",
            content="Discover different yoga practices and their benefits for physical and mental health.",
        ),
        Article(
            title="Gaming: Esports Tournaments",
            content="Stay updated on the latest esports tournaments and competitive gaming events.",
        ),
        Article(
            title="Art: Digital Art Trends",
            content="Explore the latest trends in digital art and how artists are using technology to create.",
        ),
        Article(
            title="Theater: Broadway Shows",
            content="Get information on the latest Broadway shows and theater performances.",
        ),
        Article(
            title="Photography: Advanced Techniques",
            content="Learn advanced photography techniques to take your skills to the next level.",
        ),
        Article(
            title="Gardening: Indoor Plants",
            content="Find out which indoor plants are best for your home and how to care for them.",
        ),
        Article(
            title="DIY: Craft Projects",
            content="Get inspired with these fun and creative DIY craft projects.",
        ),
        Article(
            title="Pets: Training Tips",
            content="Learn effective training tips to help your pets behave well and stay happy.",
        ),
        Article(
            title="Relationships: Communication Skills",
            content="Experts share advice on improving communication skills in relationships.",
        ),
        Article(
            title="Career: Remote Work Tips",
            content="Discover tips for staying productive and maintaining work-life balance while working remotely.",
        ),
        Article(
            title="Finance: Retirement Planning",
            content="Financial advisors provide insights on planning for a secure and comfortable retirement.",
        ),
        Article(
            title="Science: Climate Change Research",
            content="Read about the latest research on climate change and its global impact.",
        ),
        Article(
            title="Health: Sleep Hygiene",
            content="Experts discuss the importance of sleep hygiene and how to improve your sleep quality.",
        ),
        Article(
            title="Technology: Smart Home Devices",
            content="Learn about the latest smart home devices and how they can make your life easier.",
        ),
        Article(
            title="Culture: Art Festivals",
            content="Discover art festivals around the world that showcase diverse and vibrant cultures.",
        ),
        Article(
            title="Business: Leadership Skills",
            content="Read about essential leadership skills and how to develop them for business success.",
        ),
        Article(
            title="Lifestyle: Work-Life Balance",
            content="Explore strategies for achieving a healthy work-life balance in today's fast-paced world.",
        ),
    ]
    for article in articles:
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ("The_SQL_Heist_App", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_fake_articles),
    ]
