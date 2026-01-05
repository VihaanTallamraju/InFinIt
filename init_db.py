#!/usr/bin/env python3
"""
FinLit Database Initialization Script
Creates and populates the database with sample content.

Run with: python init_db.py
"""

from app import app, db, BlogPost, Book, Video, Survey
from datetime import datetime
import os

def init_database():
    """Initialize the database with sample data"""
    print("Initializing FinLit database...")
    
    # Create all tables
    with app.app_context():
        # Create all tables (will create database file if it doesn't exist)
        db.create_all()
        
        # Add sample blog posts
        add_blog_posts()
        
        # Add sample books
        add_books()
        
        # Add sample videos
        add_videos()
        
        # Add sample survey responses
        add_sample_surveys()
        
        # Commit all changes
        db.session.commit()
        
    print("Database initialized successfully!")
    print(f"Database location: {os.path.abspath('data/finlit.db')}")

def add_blog_posts():
    """Fetch and add blog posts from the external Blogger site."""
    print("Importing external blog posts from Blogger feed...")
    import json, re
    from urllib.request import urlopen
    FEED_URL = "https://vihaantallamraju-businessandstocks.blogspot.com/feeds/posts/default?alt=json"

    with app.app_context():
        # Clear existing posts to avoid duplicates
        BlogPost.query.delete()

        try:
            with urlopen(FEED_URL, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"Failed to fetch feed: {e}")
            return

        entries = data.get("feed", {}).get("entry", [])
        imported = 0
        for entry in entries:
            title = entry.get("title", {}).get("$t", "Untitled")
            published_raw = entry.get("published", {}).get("$t")
            # Try ISO parsing (Python 3.11+ handles offsets); fallback to utcnow
            try:
                from datetime import datetime as _dt
                date_posted = _dt.fromisoformat(published_raw.replace("Z", "+00:00")) if published_raw else datetime.utcnow()
            except Exception:
                date_posted = datetime.utcnow()

            content_html = entry.get("content", {}).get("$t", "")
            # Build excerpt: strip tags, collapse whitespace, truncate
            text = re.sub(r"<[^>]+>", " ", content_html)
            text = re.sub(r"\s+", " ", text).strip()
            excerpt = (text[:230] + "...") if len(text) > 230 else text

            post = BlogPost(
                title=title,
                excerpt=excerpt,
                content=content_html,
                date_posted=date_posted
            )
            db.session.add(post)
            imported += 1

        print(f"Imported {imported} blog posts from external source.")

        # Add requested specific articles explicitly (ensures visibility)
        manual_articles = [
            {
                "title": "Types of Investments",
                "url": "https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/types-of-investments.html#more",
                "excerpt": "Overview of common investment types for beginners: stocks, bonds, index funds, and more.",
                "content_html": (
                    "<p>This article explains different types of investments for beginners and how they compare." 
                    "</p><p><a href='https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/types-of-investments.html#more' "
                    "target='_blank' rel='noopener noreferrer' class='btn btn-primary'>Read on Blogger</a></p>"
                )
            },
            {
                "title": "Why Investing Is Important",
                "url": "https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/why-investing-is-important.html",
                "excerpt": "Why starting to invest early matters: compound growth, beating inflation, and building long-term wealth.",
                "content_html": (
                    "<p>This article covers why investing is important, including compound interest and long-term goals." 
                    "</p><p><a href='https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/why-investing-is-important.html' "
                    "target='_blank' rel='noopener noreferrer' class='btn btn-primary'>Read on Blogger</a></p>"
                )
            },
            {
                "title": "Needs vs Wants",
                "url": "https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/needs-vs-wants.html",
                "excerpt": "Learn to separate essential expenses from discretionary spending to improve budgeting decisions.",
                "content_html": (
                    "<p>Understand the difference between needs and wants to make smarter budgeting decisions." 
                    "</p><p><a href='https://vihaantallamraju-businessandstocks.blogspot.com/2026/01/needs-vs-wants.html' "
                    "target='_blank' rel='noopener noreferrer' class='btn btn-primary'>Read on Blogger</a></p>"
                )
            }
        ]

        # Insert manual articles if not present by title
        for art in manual_articles:
            exists = BlogPost.query.filter(BlogPost.title == art["title"]).first()
            if exists:
                continue
            post = BlogPost(
                title=art["title"],
                excerpt=art["excerpt"],
                content=art["content_html"],
                date_posted=datetime.utcnow()
            )
            db.session.add(post)
        db.session.commit()

def add_books():
    """Add sample book recommendations"""
    print("Adding book recommendations...")
    
    # Clear existing books to avoid duplication when re-running init
    Book.query.delete()
    
    books = [
        {
            "title": "The Psychology of Money",
            "author": "Morgan Housel",
            "description": "Stories showing how behavior and mindset drive financial outcomes. Builds discipline and long-term thinking.",
            "age_range": "Ages 14+"
        },
        {
            "title": "Rich Dad Poor Dad for Teens",
            "author": "Robert Kiyosaki",
            "description": "Introduces assets vs. liabilities and smarter thinking about earning and building wealth for teens.",
            "age_range": "Ages 12-18"
        },
        {
            "title": "I Will Teach You To Be Rich",
            "author": "Ramit Sethi",
            "description": "Friendly guide covering saving, budgeting, conscious spending, automation and beginner investing.",
            "age_range": "Ages 15+"
        },
        {
            "title": "The Richest Man in Babylon",
            "author": "George S. Clason",
            "description": "Short parables teaching: save first, live wisely, avoid debt traps. Timeless financial principles.",
            "age_range": "Ages 12+"
        },
        {
            "title": "The Teen Investor",
            "author": "Emmanuel Modu",
            "description": "Designed specifically for teens wanting to understand investing early while managing risk.",
            "age_range": "Ages 13-18"
        },
        {
            "title": "How to Money",
            "author": "Jean Chatzky & Kathryn Tuggle",
            "description": "Entry-level overview: savings accounts, budgeting, credit cards, simple investing and confidence.",
            "age_range": "Ages 12-20"
        },
        {
            "title": "The Simple Path to Wealth",
            "author": "JL Collins",
            "description": "Explains index funds and long-term investing simply. A foundational guide for young adults.",
            "age_range": "Ages 15+"
        },
        {
            "title": "Broke Millennial",
            "author": "Erin Lowry",
            "description": "Real-world guidance on salary, credit, debt management, and early financial independence.",
            "age_range": "Ages 16+"
        },
        {
            "title": "The Millionaire Next Door",
            "author": "Thomas J. Stanley",
            "description": "Research-based look at how ordinary families build wealth through frugality and smart choices.",
            "age_range": "Ages 15+"
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "description": "Not finance-specific but teaches habit systems that support saving, investing and discipline.",
            "age_range": "Ages 13+"
        }
    ]
    
    for book_data in books:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            description=book_data['description'],
            age_range=book_data['age_range']
        )
        db.session.add(book)

def add_videos():
    """Add sample video resources"""
    print("Adding video resources...")
    
    # Clear existing videos so we can keep only the first original and add new list
    Video.query.delete()
    
    # Keep first original video, replace rest with new 12-item list (Money basics focus)
    videos = [
        {
            "title": "One Idiot - Financial Literacy Short Film",
            "description": "Entertaining short film introducing core money management mistakes and smart habits for beginners.",
            "youtube_id": "vU1l1TB7GzI",
            "duration": "15:12"
        },
        # 1. Money basics introduction
        {
            "title": "Money Basics Introduction – Learn the Foundations of Money",
            "description": "Explains what money is, how it works, and the core ideas behind a money system.",
            "youtube_id": "GwAIu-RA_WA",
            "duration": "00:00"
        },
        # 2. Needs vs wants
        {
            "title": "Financial Literacy – Needs and Wants",
            "description": "Helps teens distinguish between needs and wants for better spending decisions.",
            "youtube_id": "aRcXutXvfmM",
            "duration": "00:00"
        },
        # 3. How to make a budget
        {
            "title": "Financial Literacy – Making a Budget",
            "description": "Step-by-step guide to building a simple budget from income and expenses.",
            "youtube_id": "cYGiipJOiLg",
            "duration": "00:00"
        },
        # 4. Saving as a teen
        {
            "title": "15 Easy Ways to Save Money as a Teen – SimplyMaci",
            "description": "Practical saving ideas teens can implement immediately in daily life.",
            "youtube_id": "o4AgSmpCFIA",
            "duration": "00:00"
        },
        # 5. What teens should learn in school
        {
            "title": "5 Money Lessons Everyone Should Learn in High School",
            "description": "Core lessons on saving, debt, interest, and investing often skipped in school.",
            "youtube_id": "GCMmn55HazM",
            "duration": "00:00"
        },
        # 6. Stock market overview
        {
            "title": "Stock Market for Beginners 2025/2026 – The Ultimate",
            "description": "Long walkthrough of how shares and the stock market work and how to start investing.",
            "youtube_id": "bb6_M_srMBk",
            "duration": "00:00"
        },
        # 7. Teen investing step by step
        {
            "title": "Teen Investing 101 – The Ultimate Step by Step Guide",
            "description": "Why to start early, account types, and first investing steps for teens.",
            "youtube_id": "V8l2JEIleZ0",
            "duration": "00:00"
        },
        # 8. Investing for teenagers in India
        {
            "title": "How To Invest For Teenagers In India? Investing Ideas For Beginners – CA Rachana Ranade",
            "description": "How Indian teens can begin investing through parents and mutual funds using local examples.",
            "youtube_id": "TGdlG9FgJeo",
            "duration": "00:00"
        },
        # 9. How compound interest works
        {
            "title": "Financial Literacy – How Does Compound Interest Work",
            "description": "Difference between simple and compound interest and why starting early matters.",
            "youtube_id": "ZJD2VrbvJ44",
            "duration": "00:00"
        },
        # 10. Credit cards explained for teens
        {
            "title": "What is a Credit Card? A Simple Explanation for Teens and Adults",
            "description": "What a credit card is, how it works, and caution around debt.",
            "youtube_id": "UjjeU-Ls8DA",
            "duration": "00:00"
        },
        # 11. Side hustles for teenagers
        {
            "title": "7 Side Hustles Teenagers Can Start in 2026",
            "description": "Modern online-friendly side hustle ideas teens can start with low cost.",
            "youtube_id": "j08BweYFcxw",
            "duration": "00:00"
        },
        # 12. Tracking money with a simple sheet
        {
            "title": "This Personal Finance Spreadsheet Changed My Life",
            "description": "Spreadsheet method for tracking income, spending, and saving.",
            "youtube_id": "ss-ufzKALnI",
            "duration": "00:00"
        }
    ]
    
    for video_data in videos:
        video = Video(
            title=video_data['title'],
            description=video_data['description'],
            youtube_id=video_data['youtube_id'],
            duration=video_data['duration']
        )
        db.session.add(video)

def add_sample_surveys():
    """Add sample survey responses for demonstration"""
    print("Adding sample survey responses...")
    
    sample_surveys = [
        {
            "age": 16,
            "financial_knowledge": 2,
            "games_rating": 5,
            "content_rating": 4,
            "favorite_topic": "budgeting",
            "suggestions": "More games about investing would be cool!"
        },
        {
            "age": 17,
            "financial_knowledge": 3,
            "games_rating": 4,
            "content_rating": 5,
            "favorite_topic": "investing",
            "suggestions": "Could you add a game about credit cards?"
        },
        {
            "age": 15,
            "financial_knowledge": 1,
            "games_rating": 5,
            "content_rating": 4,
            "favorite_topic": "saving",
            "suggestions": "The games are really helpful! Maybe add more scenarios."
        },
        {
            "age": 18,
            "financial_knowledge": 4,
            "games_rating": 3,
            "content_rating": 4,
            "favorite_topic": "college",
            "suggestions": "More content about student loans would be great."
        },
        {
            "age": 14,
            "financial_knowledge": 1,
            "games_rating": 5,
            "content_rating": 5,
            "favorite_topic": "jobs",
            "suggestions": "This app is amazing! My friends should try it too."
        }
    ]
    
    for survey_data in sample_surveys:
        survey = Survey(
            age=survey_data['age'],
            financial_knowledge=survey_data['financial_knowledge'],
            games_rating=survey_data['games_rating'],
            content_rating=survey_data['content_rating'],
            favorite_topic=survey_data['favorite_topic'],
            suggestions=survey_data['suggestions']
        )
        db.session.add(survey)

if __name__ == '__main__':
    init_database()