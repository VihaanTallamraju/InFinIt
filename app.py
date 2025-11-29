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

# Ensure all tables exist at startup to avoid 500s on first run
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        logging.error(f"DB init error: {e}")

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

class GamePlay(db.Model):
    """Game play session records for analytics and personalized feedback"""
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    metrics_json = db.Column(db.Text, nullable=False)  # Stored JSON of play metrics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GamePlay {self.game_name} {self.created_at.isoformat()}>'

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

# Investment Simulation API (reverted to simpler working version)
@app.route('/api/games/invest', methods=['POST'])
def api_invest():
    data = request.get_json() or {}
    amount = float(data.get('amount', 500))
    years = int(data.get('years', 5))
    inv_type = str(data.get('type', 'savings'))

    investments = {
        'savings': {'rate': 0.01, 'explanation': 'Savings Account: Safe and predictable, ideal for short-term goals.'},
        'index':   {'rate': 0.07, 'explanation': 'Index Fund: Diversified stock market exposure with moderate risk.'},
        'stock':   {'rate': 0.12, 'explanation': 'Individual Stock: Potentially high returns but high volatility and risk.'},
    }

    config = investments.get(inv_type, investments['savings'])
    base_rate = config['rate']

    import random
    value = amount
    annual_returns = []
    for _ in range(years):
        jitter = random.uniform(-base_rate * 0.2, base_rate * 0.2)
        rate = max(-0.3, min(0.5, base_rate + jitter))
        value = round(value * (1 + rate), 2)
        annual_returns.append(value)

    total_return = round(value - amount, 2)
    overall_rate = round(((value / amount) - 1) * 100, 2)
    explanation = config['explanation']

    try:
        gp = GamePlay(game_name='invest', metrics_json=json.dumps({
            'amount': amount,
            'years': years,
            'type': inv_type,
            'final_value': value,
            'total_return': total_return,
            'return_rate': overall_rate,
            'annual_returns': annual_returns,
        }))
        db.session.add(gp)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({
        'final_value': value,
        'total_return': total_return,
        'return_rate': overall_rate,
        'annual_returns': annual_returns,
        'explanation': explanation,
    })

@app.route('/api/games/saving', methods=['POST'])
def api_saving_game():
    """API endpoint to record Saving Sprint decisions and compute enhanced summary"""
    data = request.get_json() or {}
    decisions = data.get('decisions', [])  # list of {month, choice, monthlySavings, totalSavings}
    final_savings = float(data.get('final_savings', 0))
    goal = float(data.get('goal', 1000))
    goal_percentage = (final_savings / goal * 100) if goal > 0 else 0
    
    # Grade logic similar to client with enhancement
    if goal_percentage >= 100:
        grade = 'A+'
        base_message = 'Outstanding goal completion and disciplined saving.'
    elif goal_percentage >= 80:
        grade = 'A'
        base_message = 'Excellent progress. You are close to full emergency readiness.'
    elif goal_percentage >= 60:
        grade = 'B'
        base_message = 'Good effort. Consider tightening wants to push higher.'
    elif goal_percentage >= 40:
        grade = 'C'
        base_message = 'Moderate progress. Reevaluate discretionary spending patterns.'
    else:
        grade = 'D'
        base_message = 'Limited emergency buffer. Prioritize consistent monthly savings.'
    
    # Analyze decision patterns
    monthly_savings_values = [d.get('monthlySavings', 0) for d in decisions]
    avg_monthly = sum(monthly_savings_values) / len(monthly_savings_values) if monthly_savings_values else 0
    if len(monthly_savings_values) > 1:
        mean_val = avg_monthly
        variance = sum((v - mean_val) ** 2 for v in monthly_savings_values) / (len(monthly_savings_values) - 1)
        consistency = max(0.0, 100 - (variance ** 0.5))  # heuristic
    else:
        consistency = 100.0
    
    # Personalized pointers
    pointers = []
    if avg_monthly < goal / 12:
        pointers.append('Average monthly savings is below pace for goal; try reserving a fixed amount immediately on income receipt.')
    if consistency < 70:
        pointers.append('Savings were volatile. Setting a baseline amount each month can stabilize progress.')
    if not pointers:
        pointers.append('Great consistency and pace. Consider setting a stretch goal or allocating part to investing.')
    
    learning_summary = base_message + ' ' + ' '.join(pointers)
    
    metrics = {
        'game': 'saving',
        'final_savings': final_savings,
        'goal': goal,
        'goal_percentage': goal_percentage,
        'grade': grade,
        'avg_monthly_savings': avg_monthly,
        'consistency_score': consistency,
        'decisions': decisions
    }
    logging.info(json.dumps(metrics))
    try:
        db.session.add(GamePlay(game_name='saving', metrics_json=json.dumps(metrics)))
        db.session.commit()
    except Exception as e:
        logging.error(f"GamePlay persist error (saving): {e}")
    
    return jsonify({
        'grade': grade,
        'goal_percentage': round(goal_percentage, 1),
        'avg_monthly_savings': round(avg_monthly, 2),
        'consistency_score': round(consistency, 1),
        'learning_summary': learning_summary
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