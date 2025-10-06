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
    """Add sample blog posts"""
    print("Adding blog posts...")
    
    blog_posts = [
        {
            "title": "Your First Budget: A Teen's Guide to Money Management",
            "excerpt": "Learn how to create your very first budget and take control of your money. We'll show you simple steps that actually work for teenagers.",
            "content": """
                <h2>Why Budgeting Matters for Teens</h2>
                <p>Creating your first budget might seem scary, but it's actually one of the most empowering things you can do with your money. A budget is simply a plan for your money – it tells your dollars where to go instead of wondering where they went!</p>
                
                <h3>The 50/30/20 Rule Made Simple</h3>
                <p>Here's an easy way to split your money:</p>
                <ul>
                    <li><strong>50% for Needs:</strong> Phone bill, transportation, school supplies</li>
                    <li><strong>30% for Wants:</strong> Movies, games, clothes you don't really need</li>
                    <li><strong>20% for Savings:</strong> Emergency fund and future goals</li>
                </ul>
                
                <h3>Getting Started</h3>
                <p>Start by tracking everything you spend for one week. Write it all down – even that $2 candy bar. You might be surprised where your money actually goes!</p>
                
                <blockquote>
                "A budget is telling your money where to go instead of wondering where it went." - Dave Ramsey
                </blockquote>
                
                <p>Remember, your budget doesn't have to be perfect. The goal is to start somewhere and adjust as you learn more about your spending habits.</p>
            """
        },
        {
            "title": "Emergency Fund 101: Why Every Teen Needs One",
            "excerpt": "Life is unpredictable, and that's exactly why you need an emergency fund. Learn why starting early gives you a huge advantage.",
            "content": """
                <h2>What is an Emergency Fund?</h2>
                <p>An emergency fund is money you save specifically for unexpected expenses. Think of it as your financial safety net that catches you when life throws curveballs.</p>
                
                <h3>Teen-Friendly Emergencies</h3>
                <p>As a teenager, your emergencies might look different from adults, but they're still important:</p>
                <ul>
                    <li>Your phone breaks and you need it for work</li>
                    <li>Your car needs repairs (if you drive)</li>
                    <li>You lose your part-time job unexpectedly</li>
                    <li>A family emergency requires you to travel</li>
                    <li>Your laptop crashes and you need it for school</li>
                </ul>
                
                <h3>How Much Should You Save?</h3>
                <p>Start with a goal of <span class="highlight">$500-$1000</span>. This might seem like a lot, but remember – you're building a habit that will serve you for life.</p>
                
                <h3>Where to Keep It</h3>
                <p>Keep your emergency fund in a separate savings account. You want it to be accessible but not so easy that you're tempted to spend it on wants instead of needs.</p>
                
                <p><strong>Pro tip:</strong> Set up automatic transfers to your emergency fund. Even $25 per month adds up to $300 in a year!</p>
            """
        },
        {
            "title": "Investing Basics: Growing Your Money for the Future",
            "excerpt": "You're never too young to start investing. Learn the basics of how investing works and why time is your biggest advantage.",
            "content": """
                <h2>Why Invest as a Teen?</h2>
                <p>Investing might sound like something only adults do, but starting as a teenager gives you a superpower: time. Thanks to compound interest, money you invest now has decades to grow.</p>
                
                <h3>The Magic of Compound Interest</h3>
                <p>Imagine you invest $100 and it grows by 7% each year. After one year, you have $107. But in year two, you earn 7% on the full $107, not just your original $100. That's compound interest!</p>
                
                <h3>Investment Options for Beginners</h3>
                <ul>
                    <li><strong>Savings Account:</strong> Very safe, but low returns (around 1%)</li>
                    <li><strong>Index Funds:</strong> Moderate risk, historically good returns (around 7%)</li>
                    <li><strong>Individual Stocks:</strong> Higher risk, potentially higher returns</li>
                </ul>
                
                <h3>Getting Started</h3>
                <p>As a minor, you'll need a parent or guardian to help you open a custodial investment account. Many apps and brokerages offer these specifically for young investors.</p>
                
                <blockquote>
                "The best time to plant a tree was 20 years ago. The second best time is now." - Chinese Proverb
                </blockquote>
                
                <p>Remember: never invest money you can't afford to lose, and always do your research!</p>
            """
        },
        {
            "title": "Side Hustles for Teens: Earning Your Own Money",
            "excerpt": "Ready to make your own money? Discover legitimate ways teenagers can earn income and start building financial independence.",
            "content": """
                <h2>Why Earn Your Own Money?</h2>
                <p>Having your own income teaches valuable lessons about work, responsibility, and money management. Plus, it feels amazing to buy something with money you earned yourself!</p>
                
                <h3>Traditional Jobs for Teens</h3>
                <ul>
                    <li><strong>Retail:</strong> Clothing stores, grocery stores, fast food</li>
                    <li><strong>Food Service:</strong> Restaurants, ice cream shops, coffee shops</li>
                    <li><strong>Recreation:</strong> Movie theaters, amusement parks, sports venues</li>
                    <li><strong>Tutoring:</strong> Help younger students with subjects you excel in</li>
                </ul>
                
                <h3>Modern Side Hustles</h3>
                <ul>
                    <li><strong>Pet Sitting/Dog Walking:</strong> Use apps like Rover (with parent permission)</li>
                    <li><strong>Lawn Care:</strong> Mowing, raking, basic yard work</li>
                    <li><strong>Babysitting:</strong> After getting certified in CPR/First Aid</li>
                    <li><strong>Online Selling:</strong> Sell crafts, artwork, or items you no longer need</li>
                </ul>
                
                <h3>Managing Your Income</h3>
                <p>Once you start earning, remember to:</p>
                <ul>
                    <li>Save at least 20% of what you earn</li>
                    <li>Budget for your wants and needs</li>
                    <li>Keep track of your work expenses</li>
                    <li>Learn about taxes (yes, even teens usually need to file!)</li>
                </ul>
            """
        },
        {
            "title": "College Costs: Planning for Your Education",
            "excerpt": "College is expensive, but there are smart ways to manage the costs. Start planning now to avoid crushing debt later.",
            "content": """
                <h2>The Reality of College Costs</h2>
                <p>College is one of the biggest expenses you'll ever face. The average cost for a four-year degree can range from $40,000 to over $200,000 depending on the school and whether you live on campus.</p>
                
                <h3>Ways to Reduce College Costs</h3>
                <ul>
                    <li><strong>Community College First:</strong> Complete general education requirements for less</li>
                    <li><strong>In-State Schools:</strong> Significantly cheaper than out-of-state tuition</li>
                    <li><strong>Scholarships:</strong> Free money that doesn't need to be repaid</li>
                    <li><strong>Grants:</strong> Need-based aid that doesn't require repayment</li>
                    <li><strong>Work-Study Programs:</strong> Earn money while in school</li>
                </ul>
                
                <h3>Student Loans: Proceed with Caution</h3>
                <p>Student loans can help make college possible, but they need to be repaid with interest. Before taking loans:</p>
                <ul>
                    <li>Calculate your expected salary after graduation</li>
                    <li>Try not to borrow more than your first year's expected salary</li>
                    <li>Understand the difference between federal and private loans</li>
                    <li>Know your repayment options</li>
                </ul>
                
                <h3>Starting to Save Now</h3>
                <p>Even saving $50 per month starting at age 15 can add up to over $2,000 by the time you start college. Every dollar helps!</p>
            """
        },
        {
            "title": "Credit Cards 101: Building Credit Without Debt",
            "excerpt": "Credit cards can be useful tools or dangerous traps. Learn how to use them wisely to build credit without falling into debt.",
            "content": """
                <h2>What is Credit?</h2>
                <p>Credit is your ability to borrow money based on your promise to pay it back. Your credit score (a number between 300-850) tells lenders how trustworthy you are with borrowed money.</p>
                
                <h3>Why Credit Matters</h3>
                <p>Good credit helps you:</p>
                <ul>
                    <li>Get better interest rates on loans</li>
                    <li>Qualify for apartments</li>
                    <li>Sometimes even get better job opportunities</li>
                    <li>Access emergency funds when needed</li>
                </ul>
                
                <h3>Building Credit as a Teen</h3>
                <ul>
                    <li><strong>Authorized User:</strong> Ask a parent to add you to their card</li>
                    <li><strong>Student Credit Card:</strong> Designed for people with no credit history</li>
                    <li><strong>Secured Credit Card:</strong> You put down a deposit that becomes your credit limit</li>
                </ul>
                
                <h3>Golden Rules for Credit Cards</h3>
                <ol>
                    <li><strong>Pay the full balance every month</strong> - Never just pay the minimum</li>
                    <li><strong>Keep your usage low</strong> - Use less than 30% of your credit limit</li>
                    <li><strong>Pay on time, always</strong> - Late payments hurt your credit score</li>
                    <li><strong>Don't apply for too many cards</strong> - Each application can lower your score</li>
                </ol>
                
                <blockquote>
                "Credit cards are like chainsaws. Very useful, but dangerous in the wrong hands."
                </blockquote>
            """
        },
        {
            "title": "Needs vs Wants: Making Smart Spending Decisions",
            "excerpt": "Learning to tell the difference between needs and wants is crucial for good money management. It's trickier than you might think!",
            "content": """
                <h2>The Needs vs Wants Challenge</h2>
                <p>This sounds simple, but marketers spend billions trying to convince you that wants are actually needs. Learning to see through this is a crucial money skill.</p>
                
                <h3>True Needs (You Can't Live Without These)</h3>
                <ul>
                    <li>Food (but not necessarily restaurant food)</li>
                    <li>Shelter and basic utilities</li>
                    <li>Transportation to work/school</li>
                    <li>Basic clothing</li>
                    <li>Healthcare</li>
                </ul>
                
                <h3>Common "Fake Needs" (Really Wants in Disguise)</h3>
                <ul>
                    <li><strong>"I NEED the latest iPhone"</strong> - Any working phone meets the communication need</li>
                    <li><strong>"I NEED brand name clothes"</strong> - Any clothes that fit and are appropriate meet the need</li>
                    <li><strong>"I NEED to eat out"</strong> - Food is a need, restaurants are a convenience/want</li>
                    <li><strong>"I NEED a car"</strong> - Transportation is a need, but maybe public transit works too</li>
                </ul>
                
                <h3>The 24-Hour Rule</h3>
                <p>Before buying anything over $20, wait 24 hours. If it's over $100, wait a week. This simple pause often reveals that the "urgent need" was really just a passing want.</p>
                
                <h3>Making Room for Wants</h3>
                <p>Wants aren't bad! They make life enjoyable. The key is to:</p>
                <ol>
                    <li>Take care of needs first</li>
                    <li>Save for the future</li>
                    <li>Then enjoy some wants guilt-free</li>
                </ol>
            """
        },
        {
            "title": "Banking Basics: Choosing Your First Bank Account",
            "excerpt": "Your first bank account is an important step toward financial independence. Learn what to look for and avoid costly mistakes.",
            "content": """
                <h2>Why You Need a Bank Account</h2>
                <p>A bank account keeps your money safe, makes it easy to track spending, and helps you start building a relationship with a financial institution.</p>
                
                <h3>Types of Accounts for Teens</h3>
                <ul>
                    <li><strong>Teen Checking Account:</strong> For everyday spending, usually no fees</li>
                    <li><strong>Savings Account:</strong> For money you're not spending right away</li>
                    <li><strong>Joint Account:</strong> Shared with a parent until you turn 18</li>
                </ul>
                
                <h3>What to Look For</h3>
                <ul>
                    <li><strong>No monthly fees</strong> (or easy ways to avoid them)</li>
                    <li><strong>Free ATM access</strong> (or reimbursement for ATM fees)</li>
                    <li><strong>Online and mobile banking</strong></li>
                    <li><strong>Good customer service</strong></li>
                    <li><strong>Convenient locations</strong> (if you prefer in-person banking)</li>
                </ul>
                
                <h3>Red Flags to Avoid</h3>
                <ul>
                    <li>High monthly maintenance fees</li>
                    <li>Expensive overdraft fees</li>
                    <li>Limited ATM access</li>
                    <li>Poor online reviews</li>
                </ul>
                
                <h3>Banking Tips for Beginners</h3>
                <ol>
                    <li><strong>Track your balance</strong> - Use the bank app or write it down</li>
                    <li><strong>Set up account alerts</strong> - Get notified of low balances</li>
                    <li><strong>Understand fees</strong> - Read the fine print</li>
                    <li><strong>Keep receipts</strong> - Check them against your account</li>
                </ol>
            """
        },
        {
            "title": "Money and Friends: Navigating Social Spending Pressure",
            "excerpt": "Friends can influence your spending in ways you might not realize. Learn how to handle money situations with friends while staying true to your budget.",
            "content": """
                <h2>The Social Side of Money</h2>
                <p>Money affects friendships more than we like to admit. Learning to handle these situations now will save you stress and money throughout your life.</p>
                
                <h3>Common Social Money Challenges</h3>
                <ul>
                    <li>Friends want to go somewhere expensive</li>
                    <li>Pressure to split bills equally when you ordered less</li>
                    <li>Being asked to lend money</li>
                    <li>Feeling left out because you can't afford activities</li>
                    <li>Friends who always "forget" their wallet</li>
                </ul>
                
                <h3>Strategies That Work</h3>
                <ul>
                    <li><strong>Be honest about your budget:</strong> "That sounds fun, but it's not in my budget this month"</li>
                    <li><strong>Suggest alternatives:</strong> "What if we hung out at the park instead?"</li>
                    <li><strong>Plan ahead:</strong> "I can go, but I need to save up for it"</li>
                    <li><strong>Separate bills:</strong> "Could we get separate checks?"</li>
                </ul>
                
                <h3>The Lending Money Dilemma</h3>
                <p>Lending money to friends can damage relationships. If you choose to lend money:</p>
                <ul>
                    <li>Only lend what you can afford to lose</li>
                    <li>Be clear about when you expect it back</li>
                    <li>Consider it a gift to preserve the friendship</li>
                </ul>
                
                <h3>Finding Your Money Tribe</h3>
                <p>Surround yourself with friends who respect your financial goals. Good friends will understand when you say no and won't pressure you to overspend.</p>
                
                <blockquote>
                "You are the average of the five people you spend the most time with." - Jim Rohn
                </blockquote>
            """
        },
        {
            "title": "Summer Job Success: Making the Most of Seasonal Work",
            "excerpt": "Summer jobs are a great way to earn money and gain experience. Learn how to find good opportunities and make your summer work count.",
            "content": """
                <h2>Why Summer Jobs Rock</h2>
                <p>Summer jobs offer more than just money. They provide work experience, help you develop skills, and can even help you figure out what you want (or don't want) to do as a career.</p>
                
                <h3>Popular Summer Jobs for Teens</h3>
                <ul>
                    <li><strong>Retail:</strong> Clothing stores often hire seasonal help</li>
                    <li><strong>Food Service:</strong> Ice cream shops, restaurants, food trucks</li>
                    <li><strong>Recreation:</strong> Pools, camps, amusement parks</li>
                    <li><strong>Landscaping:</strong> Lawn care, gardening, outdoor maintenance</li>
                    <li><strong>Tutoring:</strong> Help younger kids who need summer academic support</li>
                </ul>
                
                <h3>Job Hunting Tips</h3>
                <ol>
                    <li><strong>Start early:</strong> Begin looking in March/April</li>
                    <li><strong>Apply everywhere:</strong> Don't put all your eggs in one basket</li>
                    <li><strong>Follow up:</strong> Check back a week after applying</li>
                    <li><strong>Be flexible:</strong> Available weekends and evenings = more hours</li>
                    <li><strong>Dress appropriately:</strong> Even for a casual job interview</li>
                </ol>
                
                <h3>Making Your Money Work</h3>
                <p>Don't blow your whole summer paycheck! Try this split:</p>
                <ul>
                    <li><strong>50% Save:</strong> For college, car, or other big goals</li>
                    <li><strong>30% Spend:</strong> On fun things you want</li>
                    <li><strong>20% Give/Invest:</strong> Charity or start investing</li>
                </ul>
                
                <h3>Building Your Resume</h3>
                <p>Even a "simple" summer job teaches valuable skills:</p>
                <ul>
                    <li>Customer service</li>
                    <li>Teamwork and communication</li>
                    <li>Time management</li>
                    <li>Problem-solving</li>
                    <li>Responsibility and reliability</li>
                </ul>
            """
        },
        {
            "title": "Financial Apps for Teens: Technology Meets Money Management",
            "excerpt": "The right apps can make managing money easier and more fun. Discover teen-friendly financial apps that actually help (and which ones to avoid).",
            "content": """
                <h2>Why Use Financial Apps?</h2>
                <p>Good financial apps can help you track spending, save money automatically, and learn about investing. But with so many options, how do you choose the right ones?</p>
                
                <h3>Categories of Helpful Apps</h3>
                
                <h4>Budgeting and Tracking</h4>
                <ul>
                    <li><strong>Mint:</strong> Free budgeting and expense tracking</li>
                    <li><strong>YNAB (You Need A Budget):</strong> More advanced budgeting (free for students)</li>
                    <li><strong>Goodbudget:</strong> Digital envelope system</li>
                </ul>
                
                <h4>Saving Apps</h4>
                <ul>
                    <li><strong>Qapital:</strong> Rounds up purchases and saves the change</li>
                    <li><strong>Digit:</strong> Automatically saves small amounts</li>
                    <li><strong>SmartyPig:</strong> Goal-based savings</li>
                </ul>
                
                <h4>Teen-Specific Banking</h4>
                <ul>
                    <li><strong>Greenlight:</strong> Debit card with parental controls</li>
                    <li><strong>Copper Banking:</strong> Designed specifically for teens</li>
                    <li><strong>GoHenry:</strong> Prepaid card with spending controls</li>
                </ul>
                
                <h3>Red Flags to Avoid</h3>
                <ul>
                    <li>Apps that charge high fees</li>
                    <li>Anything promising "get rich quick"</li>
                    <li>Apps without proper security measures</li>
                    <li>Services that seem too good to be true</li>
                </ul>
                
                <h3>Security Tips</h3>
                <ol>
                    <li>Never share login information</li>
                    <li>Use strong, unique passwords</li>
                    <li>Enable two-factor authentication</li>
                    <li>Only download apps from official app stores</li>
                    <li>Read reviews and research companies</li>
                </ol>
                
                <p>Remember: Apps are tools to help you manage money, not magic solutions. You still need to make smart financial decisions!</p>
            """
        },
        {
            "title": "Taxes for Teens: Yes, You Might Need to File!",
            "excerpt": "Many teens are surprised to learn they need to file taxes. Get the basics on teen tax requirements and how to handle your first tax return.",
            "content": """
                <h2>Do Teens Really Pay Taxes?</h2>
                <p>Yes! If you earn money, you'll likely need to pay taxes and possibly file a tax return. The good news? Teen tax situations are usually pretty simple.</p>
                
                <h3>When You Must File</h3>
                <p>For 2024, you generally need to file if you earned:</p>
                <ul>
                    <li><strong>More than $13,850</strong> from a job (W-2 income)</li>
                    <li><strong>More than $1,250</strong> from investments or self-employment</li>
                    <li><strong>Any amount</strong> if taxes were withheld and you want a refund</li>
                </ul>
                
                <h3>Understanding Your Paycheck</h3>
                <p>Look at your paycheck stub - you'll see deductions for:</p>
                <ul>
                    <li><strong>Federal Income Tax:</strong> Goes to the federal government</li>
                    <li><strong>State Income Tax:</strong> Goes to your state (if applicable)</li>
                    <li><strong>Social Security:</strong> 6.2% of your pay</li>
                    <li><strong>Medicare:</strong> 1.45% of your pay</li>
                </ul>
                
                <h3>Filing Your Return</h3>
                <p>Filing taxes as a teen is usually straightforward:</p>
                <ol>
                    <li>Gather your W-2 forms (from employers)</li>
                    <li>Use free tax software (many are free for simple returns)</li>
                    <li>Enter your income information</li>
                    <li>Submit before the deadline (usually April 15)</li>
                </ol>
                
                <h3>Can Your Parents Claim You?</h3>
                <p>If your parents provide more than half your support, they can usually claim you as a dependent. This means:</p>
                <ul>
                    <li>They get a tax benefit</li>
                    <li>You can't claim yourself</li>
                    <li>You might still get a refund if too much was withheld</li>
                </ul>
                
                <h3>Tax Tips for Teens</h3>
                <ul>
                    <li>Keep all tax documents (W-2s, 1099s)</li>
                    <li>File even if you don't owe taxes (to get refunds)</li>
                    <li>Consider having a parent help with your first return</li>
                    <li>Use free tax preparation resources</li>
                </ul>
            """
        },
        {
            "title": "Goal Setting: Turning Money Dreams into Reality",
            "excerpt": "Having financial goals gives your money purpose. Learn how to set realistic goals and create a plan to achieve them.",
            "content": """
                <h2>Why Financial Goals Matter</h2>
                <p>Without goals, money just disappears on random stuff. With clear goals, every dollar has a purpose, and you'll be amazed at what you can accomplish.</p>
                
                <h3>Types of Financial Goals</h3>
                
                <h4>Short-term (1-6 months)</h4>
                <ul>
                    <li>Buy a new phone or laptop</li>
                    <li>Save for a school trip</li>
                    <li>Build a $500 emergency fund</li>
                    <li>Buy a gift for someone special</li>
                </ul>
                
                <h4>Medium-term (6 months - 2 years)</h4>
                <ul>
                    <li>Save for a car</li>
                    <li>Build a $2,000 emergency fund</li>
                    <li>Save for senior year expenses</li>
                    <li>Fund a summer vacation</li>
                </ul>
                
                <h4>Long-term (2+ years)</h4>
                <ul>
                    <li>College fund</li>
                    <li>First apartment deposit</li>
                    <li>Start investing for retirement</li>
                    <li>Business startup fund</li>
                </ul>
                
                <h3>SMART Goal Framework</h3>
                <p>Make your goals SMART:</p>
                <ul>
                    <li><strong>Specific:</strong> "Save for a MacBook Pro" not "save money"</li>
                    <li><strong>Measurable:</strong> "$1,200" not "a lot"</li>
                    <li><strong>Achievable:</strong> Realistic based on your income</li>
                    <li><strong>Relevant:</strong> Important to you personally</li>
                    <li><strong>Time-bound:</strong> "by graduation" not "someday"</li>
                </ul>
                
                <h3>Creating Your Action Plan</h3>
                <ol>
                    <li><strong>Calculate the total cost</strong> (including tax if applicable)</li>
                    <li><strong>Set your deadline</strong></li>
                    <li><strong>Divide by months</strong> to get your monthly savings target</li>
                    <li><strong>Find the money</strong> in your budget</li>
                    <li><strong>Track your progress</strong> monthly</li>
                </ol>
                
                <h3>Staying Motivated</h3>
                <ul>
                    <li>Put a picture of your goal somewhere you'll see it daily</li>
                    <li>Track progress visually (charts, apps)</li>
                    <li>Celebrate milestones (25%, 50%, 75% complete)</li>
                    <li>Tell friends and family about your goals for accountability</li>
                </ul>
                
                <blockquote>
                "A goal without a plan is just a wish." - Antoine de Saint-Exupéry
                </blockquote>
            """
        },
        {
            "title": "Money Mistakes to Avoid: Learn from Others' Expensive Lessons",
            "excerpt": "Everyone makes money mistakes, but you don't have to make them all yourself. Learn the most common financial errors and how to avoid them.",
            "content": """
                <h2>Why Learn from Others' Mistakes?</h2>
                <p>Making your own mistakes is one way to learn, but it's expensive! Learning from others' mistakes is much cheaper and less stressful.</p>
                
                <h3>Top Money Mistakes Teens Make</h3>
                
                <h4>1. Not Having a Budget</h4>
                <p><strong>The mistake:</strong> Spending without tracking where money goes</p>
                <p><strong>The fix:</strong> Track expenses for one week, then create a simple budget</p>
                
                <h4>2. Buying on Impulse</h4>
                <p><strong>The mistake:</strong> Seeing something and buying it immediately</p>
                <p><strong>The fix:</strong> Wait 24 hours before buying anything over $20</p>
                
                <h4>3. Not Saving Anything</h4>
                <p><strong>The mistake:</strong> "I don't make enough to save"</p>
                <p><strong>The fix:</strong> Save something, even if it's just $5 per week</p>
                
                <h4>4. Comparing Yourself to Others</h4>
                <p><strong>The mistake:</strong> Trying to keep up with friends who have more money</p>
                <p><strong>The fix:</strong> Focus on your own goals and budget</p>
                
                <h4>5. Not Understanding Interest</h4>
                <p><strong>The mistake:</strong> Not knowing how loans and credit work</p>
                <p><strong>The fix:</strong> Learn about interest before you need to borrow money</p>
                
                <h3>Credit Card Mistakes to Avoid</h3>
                <ul>
                    <li><strong>Only paying the minimum</strong> - You'll pay way more in interest</li>
                    <li><strong>Maxing out cards</strong> - Hurts your credit score</li>
                    <li><strong>Getting too many cards</strong> - Hard to manage and track</li>
                    <li><strong>Using credit for emergencies</strong> - Build an emergency fund instead</li>
                </ul>
                
                <h3>Investment Mistakes to Avoid</h3>
                <ul>
                    <li><strong>Trying to time the market</strong> - Even experts can't do this consistently</li>
                    <li><strong>Putting all money in one investment</strong> - Diversification reduces risk</li>
                    <li><strong>Falling for get-rich-quick schemes</strong> - If it sounds too good to be true, it probably is</li>
                    <li><strong>Letting emotions drive decisions</strong> - Fear and greed are bad investment advisors</li>
                </ul>
                
                <h3>How to Recover from Money Mistakes</h3>
                <ol>
                    <li><strong>Acknowledge it</strong> - Don't ignore the problem</li>
                    <li><strong>Learn from it</strong> - What will you do differently?</li>
                    <li><strong>Make a plan</strong> - How will you fix the situation?</li>
                    <li><strong>Take action</strong> - Start making changes immediately</li>
                    <li><strong>Forgive yourself</strong> - Everyone makes mistakes</li>
                </ol>
            """
        },
        {
            "title": "Building Wealth Early: The Teenager's Secret Advantage",
            "excerpt": "Starting your wealth-building journey as a teenager gives you a massive advantage. Here's how to use time as your secret weapon.",
            "content": """
                <h2>Time: Your Greatest Asset</h2>
                <p>As a teenager, you have something that wealthy adults would pay millions for: time. Starting your wealth-building journey now gives you decades for your money to grow.</p>
                
                <h3>The Power of Starting Early</h3>
                <p>Let's compare two people:</p>
                <ul>
                    <li><strong>Sarah starts at 16:</strong> Saves $50/month until age 26, then stops</li>
                    <li><strong>Mike starts at 26:</strong> Saves $100/month until age 65</li>
                </ul>
                <p>Assuming 7% annual returns, Sarah ends up with more money at 65, even though she saved less and stopped earlier. That's the power of compound interest!</p>
                
                <h3>Wealth-Building Steps for Teens</h3>
                
                <h4>Step 1: Build Your Foundation</h4>
                <ul>
                    <li>Open a savings account</li>
                    <li>Create a budget</li>
                    <li>Start an emergency fund</li>
                    <li>Learn about money</li>
                </ul>
                
                <h4>Step 2: Increase Your Income</h4>
                <ul>
                    <li>Get a part-time job</li>
                    <li>Develop valuable skills</li>
                    <li>Start a small business</li>
                    <li>Invest in your education</li>
                </ul>
                
                <h4>Step 3: Start Investing</h4>
                <ul>
                    <li>Open a custodial investment account</li>
                    <li>Start with index funds</li>
                    <li>Reinvest dividends</li>
                    <li>Stay consistent</li>
                </ul>
                
                <h3>The Millionaire Mindset</h3>
                <p>Building wealth isn't about making tons of money (though that helps). It's about:</p>
                <ul>
                    <li><strong>Living below your means</strong> - Spend less than you earn</li>
                    <li><strong>Investing the difference</strong> - Put extra money to work</li>
                    <li><strong>Being patient</strong> - Wealth builds over decades, not days</li>
                    <li><strong>Staying educated</strong> - Keep learning about money</li>
                </ul>
                
                <h3>Avoiding Get-Rich-Quick Traps</h3>
                <p>Beware of anything promising:</p>
                <ul>
                    <li>"Make $1000 a day from home!"</li>
                    <li>Guaranteed high returns with no risk</li>
                    <li>Secret investment strategies</li>
                    <li>Cryptocurrency get-rich-quick schemes</li>
                </ul>
                
                <h3>Your 10-Year Wealth Plan</h3>
                <ol>
                    <li><strong>Years 1-2:</strong> Learn basics, build emergency fund</li>
                    <li><strong>Years 3-4:</strong> Increase income, start investing small amounts</li>
                    <li><strong>Years 5-6:</strong> College/career preparation, keep investing</li>
                    <li><strong>Years 7-8:</strong> Start career, increase investment contributions</li>
                    <li><strong>Years 9-10:</strong> Optimize taxes, diversify investments</li>
                </ol>
                
                <blockquote>
                "Someone's sitting in the shade today because someone planted a tree a long time ago." - Warren Buffett
                </blockquote>
            """
        }
    ]
    
    for post_data in blog_posts:
        post = BlogPost(
            title=post_data['title'],
            excerpt=post_data['excerpt'],
            content=post_data['content'],
            date_posted=datetime.utcnow()
        )
        db.session.add(post)

def add_books():
    """Add sample book recommendations"""
    print("Adding book recommendations...")
    
    books = [
        {
            "title": "The Richest Man in Babylon",
            "author": "George S. Clason",
            "description": "Classic financial wisdom told through parables from ancient Babylon. Easy to read and full of timeless money principles that still work today.",
            "age_range": "Ages 14+"
        },
        {
            "title": "The Teenage Investor",
            "author": "Timothy Olsen",
            "description": "Written specifically for teens, this book covers basics of investing, saving, and building wealth starting at a young age.",
            "age_range": "Ages 13-18"
        },
        {
            "title": "Smart Money Smart Kids",
            "author": "Dave Ramsey & Rachel Cruze",
            "description": "A parent-teen guide to financial literacy that covers budgeting, saving, and avoiding debt. Great for families to read together.",
            "age_range": "Ages 15+"
        },
        {
            "title": "The Index Card",
            "author": "Helaine Olen & Harold Pollack",
            "description": "All the financial advice you need fits on one index card. Simple, no-nonsense approach to personal finance that's perfect for beginners.",
            "age_range": "Ages 16+"
        },
        {
            "title": "A Random Walk Down Wall Street (Teen Edition)",
            "author": "Burton Malkiel & Charles Ellis",
            "description": "Investing basics made accessible for young people. Covers index funds, diversification, and long-term thinking.",
            "age_range": "Ages 16+"
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
    
    videos = [
        {
            "title": "Budgeting 101 for Teenagers",
            "description": "Learn the basics of creating your first budget with simple, practical steps you can start using today.",
            "youtube_id": "dQw4w9WgXcQ",  # Placeholder - replace with actual educational video IDs
            "duration": "8:32"
        },
        {
            "title": "Why You Need an Emergency Fund (Even as a Teen)",
            "description": "Discover why emergency funds are crucial for teenagers and how to start building yours with small, manageable amounts.",
            "youtube_id": "dQw4w9WgXcQ",  # Placeholder
            "duration": "6:15"
        },
        {
            "title": "Compound Interest Explained Simply",
            "description": "See the magic of compound interest in action and understand why starting early gives you a huge advantage.",
            "youtube_id": "dQw4w9WgXcQ",  # Placeholder
            "duration": "10:45"
        },
        {
            "title": "Credit Cards: Friend or Foe for Teens?",
            "description": "Learn how credit cards work, how to use them responsibly, and how to build credit without falling into debt.",
            "youtube_id": "dQw4w9WgXcQ",  # Placeholder
            "duration": "12:20"
        },
        {
            "title": "Side Hustles That Actually Work for Teenagers",
            "description": "Explore legitimate ways teens can earn money, from traditional jobs to modern gig economy opportunities.",
            "youtube_id": "dQw4w9WgXcQ",  # Placeholder
            "duration": "14:10"
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