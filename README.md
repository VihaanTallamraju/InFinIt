# FinLit - Financial Literacy for Teenagers 

A comprehensive web application designed to teach financial literacy to teenagers (ages 13-18) through interactive games, educational content, and engaging resources.

## Features

### Interactive Mini-Games
- **Budget Challenge**: Learn to allocate monthly income between needs and wants
- **Saving Sprint**: Navigate 6 months of financial decisions to build an emergency fund  
- **Investment Simulation**: Compare different investment options and see how money grows over time

### Educational Content
- **Blog**: 15+ articles covering essential financial topics written for teens
- **Book Corner**: Curated recommendations of age-appropriate financial literacy books
- **Video Library**: Embedded educational videos explaining money concepts
- **Survey System**: Collect user feedback to improve the app

### Key Learning Topics
- Budgeting and expense tracking
- Emergency funds and saving strategies  
- Investment basics and compound interest
- Credit cards and building credit
- College costs and student loans
- Side hustles and earning money
- Tax basics for teens

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd FinLit
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv finlit-env
   
   # On Windows:
   finlit-env\Scripts\activate
   
   # On macOS/Linux:
   source finlit-env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database with sample data**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:5000` to start using FinLit!

## How to Use

### For Students
1. **Start with Games**: Try the Budget Challenge to learn basic money allocation
2. **Read Articles**: Browse the blog for detailed explanations of financial concepts
3. **Watch Videos**: Visual learners can explore the embedded video content
4. **Explore Books**: Check out recommended reading for deeper learning
5. **Give Feedback**: Use the survey to help improve the app

### For Educators/Parents
- Use the admin panel (`/admin/survey-results?code=admin123`) to view aggregated feedback
- Games provide immediate feedback and can be used for classroom activities
- All content is designed to be age-appropriate and engaging for teens

## Game Mechanics

### Budget Challenge
- **Objective**: Allocate $900 monthly income between needs and wants while maximizing savings
- **Learning**: Distinguishing between needs vs wants, savings rate importance
- **Scoring**: Based on percentage saved (20%+ = excellent, 10%+ = good, etc.)

### Saving Sprint  
- **Objective**: Build a $1000 emergency fund over 6 months while handling unexpected events
- **Learning**: Emergency fund importance, making financial trade-offs
- **Mechanics**: Monthly scenarios with 3 choice options each, progress tracking

### Investment Simulation
- **Objective**: Compare savings accounts, index funds, and individual stocks
- **Learning**: Risk vs reward, compound interest, time value of money
- **Features**: Adjustable investment amount and time horizon, realistic return simulations

##  Project Structure

```
FinLit/
├── app.py                 # Main Flask application
├── init_db.py            # Database initialization script
├── test_smoke.py          # Smoke tests for basic functionality
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   ├── finlit.db         # SQLite database (created when you run the app)
│   └── plays.log         # Game play logging
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS styling
│   └── js/
│       └── games.js      # Interactive game functionality
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page
│   ├── games.html        # Games overview
│   ├── game_budget.html  # Budget Challenge game
│   ├── game_saving.html  # Saving Sprint game
│   ├── game_invest.html  # Investment Simulation game
│   ├── blog_list.html    # Blog posts list
│   ├── blog_post.html    # Individual blog post
│   ├── books.html        # Book recommendations
│   ├── videos.html       # Video resources
│   ├── survey.html       # User feedback form
│   └── admin_*.html      # Admin dashboard templates
└── .github/
    └── copilot-instructions.md
```

## Testing

Run the smoke tests to verify everything works:

```bash
python test_smoke.py
```

Tests cover:
- All page routes load correctly
- Game APIs function properly  
- Database operations work
- Form submissions process correctly
- Admin access controls function

## Technical Details

### Backend
- **Flask 3.0.0**: Web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (file-based, no setup required)

### Frontend  
- **Bootstrap 5**: Responsive CSS framework (loaded via CDN)
- **Vanilla JavaScript**: Interactive game logic
- **Jinja2**: Template engine

### Database Schema
- **BlogPost**: Articles with title, content, excerpt, date
- **Book**: Recommendations with title, author, description, age range
- **Video**: YouTube embeds with title, description, duration
- **Survey**: User feedback with ratings and suggestions

## Design Choices

### Educational Philosophy
- **Learning by Doing**: Games provide hands-on practice
- **Immediate Feedback**: Users see results of their financial decisions right away  
- **Age-Appropriate**: Content written specifically for teenagers
- **Progressive Difficulty**: Start simple, build complexity

### Technical Decisions
- **SQLite**: Simple, file-based database requiring no configuration
- **Bootstrap CDN**: Reduces bundle size, ensures responsive design
- **Vanilla JS**: Keeps dependencies minimal, easier to understand
- **Flask**: Lightweight, perfect for educational projects

### Game Design
- **Realistic Scenarios**: Based on actual teen financial situations
- **Multiple Attempts**: Users can replay games to try different strategies
- **Progress Tracking**: Local storage remembers games played
- **Visual Feedback**: Charts, progress bars, and color coding

## Sample Data

The `init_db.py` script populates the database with:
- **15 blog posts** covering budgeting, saving, investing, credit, jobs, and more
- **5 book recommendations** appropriate for teenagers  
- **5 educational videos** (placeholder YouTube IDs - replace with real content)
- **5 sample survey responses** for testing the admin dashboard

## Customization

### Adding New Content
1. **Blog Posts**: Add entries to the `add_blog_posts()` function in `init_db.py`
2. **Books**: Modify the `add_books()` function with new recommendations
3. **Videos**: Update `add_videos()` with real YouTube video IDs
4. **Games**: Extend game logic in the respective template files

### Configuration
- **Access Code**: Change admin access code in `app.py` (search for `admin123`)
- **Game Parameters**: Adjust investment returns, income amounts in game APIs
- **Styling**: Modify `static/css/style.css` for visual customization

### Database Reset
To reset the database with fresh sample data:
```bash
python init_db.py
```

## Security Notes

### For Production Use
- Change the Flask secret key in `app.py`
- Use environment variables for sensitive configuration
- Implement proper authentication for admin pages
- Add CSRF protection for forms
- Use HTTPS in production

### Current Security
- Admin pages protected with simple access code
- No personal information collected without consent
- Client-side data stored in local storage only
- SQL injection protected by SQLAlchemy ORM

## Mobile Support

The app is fully responsive and works on:
- Desktop computers
- Tablets  
- Mobile phones
- All modern browsers

Bootstrap 5 ensures consistent experience across devices.

## Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

**Database issues**
```bash
# Reinitialize the database
python init_db.py
```

**Port already in use**
```bash
# The app runs on port 5000 by default
# Kill other processes or change the port in app.py
```

**Games not working**
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled
- Try refreshing the page

### Getting Help
- Check the test results: `python test_smoke.py`
- Look for error messages in the terminal where you ran `python app.py`
- Verify all files are in the correct locations per the project structure

## Educational Use

### For Teachers
- Games can be used as classroom activities
- Blog content serves as supplementary reading
- Survey data helps assess student engagement
- Progress tracking motivates continued use

### Learning Outcomes
Students will understand:
- Basic budgeting principles
- Importance of emergency funds
- Investment fundamentals  
- Credit and debt management
- Goal setting and planning

### Assessment Ideas
- Have students play each game and discuss results
- Assign blog posts as reading with comprehension questions
- Use survey feedback to guide classroom discussions
- Create competitions around game scores

## Future Enhancements

### Potential Additions
- **More Games**: Credit card simulator, career planning tool, tax calculator
- **User Accounts**: Save progress, track learning over time
- **Multiplayer**: Compete with friends on financial challenges
- **Achievements**: Badges for completing games and reading content
- **Mobile App**: Native iOS/Android versions
- **Advanced Content**: Options trading, cryptocurrency basics, real estate

### Contributing
This is an educational project. Suggestions for improvements:
1. More realistic game scenarios
2. Additional financial topics
3. Better mobile optimization  
4. Accessibility improvements
5. Multi-language support

## License

This project is designed for educational use. Feel free to modify and adapt for your specific needs.

## Support

For questions or issues:
1. Check this README thoroughly
2. Run the smoke tests to identify problems
3. Review the code comments for implementation details
4. Test with different browsers if experiencing issues

---

**Built with love for the next generation of financially literate teenagers!**

*Remember: The best time to learn about money is right now. Start your financial literacy journey today!*
