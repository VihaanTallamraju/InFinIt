from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import logging

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'finlit-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'data', 'finlit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configure logging for game plays
if not os.path.exists('data'):
    os.makedirs('data')

logging.basicConfig(
    filename='data/plays.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Database Models
class BlogPost(db.Model):
    """Blog post model for financial literacy articles"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Book(db.Model):
    """Book recommendation model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    age_range = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Video(db.Model):
    """Video resource model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    youtube_id = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<Video {self.title}>'

class Survey(db.Model):
    """User survey responses"""
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    financial_knowledge = db.Column(db.Integer, nullable=False)  # 1-5 scale
    games_rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    content_rating = db.Column(db.Integer, nullable=False)  # 1-5 scale
    favorite_topic = db.Column(db.String(50), nullable=False)
    suggestions = db.Column(db.Text)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Survey {self.id} - Age {self.age}>'

# Routes
@app.route('/')
def index():
    """Home page with overview of all features"""
    return render_template('index.html')

@app.route('/games')
def games():
    """Games overview page"""
    return render_template('games.html')

@app.route('/games/budget')
def game_budget():
    """Budget Challenge game"""
    return render_template('game_budget.html')

@app.route('/games/saving')
def game_saving():
    """Saving Sprint game"""
    return render_template('game_saving.html')

@app.route('/games/invest')
def game_invest():
    """Investment Simulation game"""
    return render_template('game_invest.html')

@app.route('/api/games/budget', methods=['POST'])
def api_budget_game():
    """API endpoint for budget game scoring"""
    data = request.get_json()
    
    income = float(data.get('income', 0))
    expenses = data.get('expenses', {})
    
    total_expenses = sum(float(v) for v in expenses.values())
    savings = income - total_expenses
    savings_rate = (savings / income * 100) if income > 0 else 0
    
    # Calculate score based on savings rate
    if savings_rate >= 20:
        score = 100
        message = "Excellent! You're saving 20% or more. That's fantastic financial planning!"
    elif savings_rate >= 10:
        score = 80
        message = "Good job! Try to save a bit more if possible. Aim for 20% savings."
    elif savings_rate >= 5:
        score = 60
        message = "Not bad, but you could save more. Look for expenses to cut back on."
    elif savings_rate >= 0:
        score = 40
        message = "You're spending everything you earn. Try to reduce some expenses."
    else:
        score = 20
        message = "You're overspending! You need to cut back on expenses immediately."
    
    # Log game play
    logging.info(json.dumps({
        'game': 'budget',
        'income': income,
        'expenses': expenses,
        'savings': savings,
        'savings_rate': savings_rate,
        'score': score
    }))
    
    return jsonify({
        'score': score,
        'savings': round(savings, 2),
        'savings_rate': round(savings_rate, 1),
        'message': message
    })

@app.route('/api/games/invest', methods=['POST'])
def api_invest_game():
    """API endpoint for investment simulation"""
    import random
    
    data = request.get_json()
    investment_type = data.get('type', 'savings')
    amount = float(data.get('amount', 0))
    years = int(data.get('years', 1))
    
    # Define investment parameters
    investments = {
        'savings': {'rate': 0.01, 'risk': 0.002},
        'index': {'rate': 0.07, 'risk': 0.15},
        'stock': {'rate': 0.12, 'risk': 0.30}
    }
    
    params = investments.get(investment_type, investments['savings'])
    base_rate = params['rate']
    risk = params['risk']
    
    # Simulate returns with some randomness
    annual_returns = []
    current_value = amount
    
    for year in range(years):
        # Add random variance based on risk
        variance = random.uniform(-risk, risk)
        annual_rate = base_rate + variance
        current_value *= (1 + annual_rate)
        annual_returns.append(round(current_value, 2))
    
    final_value = round(current_value, 2)
    total_return = round(final_value - amount, 2)
    return_rate = round((final_value / amount - 1) * 100, 1) if amount > 0 else 0
    
    # Generate explanation
    explanations = {
        'savings': f"Savings accounts are very safe but offer low returns. Your money grew steadily at about 1% per year.",
        'index': f"Index funds offer moderate risk and returns. Over {years} year(s), you experienced some ups and downs but generally positive growth.",
        'stock': f"Individual stocks are risky but can offer high returns. Your investment experienced significant volatility over {years} year(s)."
    }
    
    # Log game play
    logging.info(json.dumps({
        'game': 'invest',
        'type': investment_type,
        'amount': amount,
        'years': years,
        'final_value': final_value,
        'return_rate': return_rate
    }))
    
    return jsonify({
        'final_value': final_value,
        'total_return': total_return,
        'return_rate': return_rate,
        'annual_returns': annual_returns,
        'explanation': explanations[investment_type]
    })

@app.route('/blog')
def blog_list():
    """Blog post list page"""
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog_list.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    """Individual blog post page"""
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/books')
def books():
    """Book recommendations page"""
    book_list = Book.query.all()
    return render_template('books.html', books=book_list)

@app.route('/videos')
def videos():
    """Video resources page"""
    video_list = Video.query.all()
    return render_template('videos.html', videos=video_list)

@app.route('/survey')
def survey():
    """User feedback survey page"""
    return render_template('survey.html')

@app.route('/survey', methods=['POST'])
def submit_survey():
    """Handle survey submission"""
    survey_data = Survey(
        age=int(request.form['age']),
        financial_knowledge=int(request.form['financial_knowledge']),
        games_rating=int(request.form['games_rating']),
        content_rating=int(request.form['content_rating']),
        favorite_topic=request.form['favorite_topic'],
        suggestions=request.form.get('suggestions', '')
    )
    
    db.session.add(survey_data)
    db.session.commit()
    
    flash('Thank you for your feedback! Your responses help us improve the app.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/survey-results')
def admin_survey_results():
    """Admin page to view survey results"""
    # Simple access control (in production, use proper authentication)
    access_code = request.args.get('code')
    if access_code != 'admin123':
        return render_template('admin_access.html')
    
    surveys = Survey.query.all()
    
    # Calculate summary statistics
    if surveys:
        avg_age = sum(s.age for s in surveys) / len(surveys)
        avg_financial_knowledge = sum(s.financial_knowledge for s in surveys) / len(surveys)
        avg_games_rating = sum(s.games_rating for s in surveys) / len(surveys)
        avg_content_rating = sum(s.content_rating for s in surveys) / len(surveys)
        
        # Count favorite topics
        topic_counts = {}
        for survey in surveys:
            topic = survey.favorite_topic
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        summary = {
            'total_responses': len(surveys),
            'avg_age': round(avg_age, 1),
            'avg_financial_knowledge': round(avg_financial_knowledge, 1),
            'avg_games_rating': round(avg_games_rating, 1),
            'avg_content_rating': round(avg_content_rating, 1),
            'topic_counts': topic_counts
        }
    else:
        summary = None
    
    return render_template('admin_survey_results.html', surveys=surveys, summary=summary)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=5001)