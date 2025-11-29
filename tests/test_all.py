#!/usr/bin/env python3
"""
FinLit Smoke Tests
Basic functionality tests to ensure the application works correctly.

Run with: python test_smoke.py
"""

import unittest
import sys
import os
import json
from unittest.mock import patch

# Add the parent directory to the path so we can import our app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db, BlogPost, Book, Video, Survey

class FinLitSmokeTests(unittest.TestCase):
    """Smoke tests for the FinLit application"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            self._add_test_data()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _add_test_data(self):
        """Add minimal test data to the database"""
        # Add a test blog post
        blog_post = BlogPost(
            title="Test Blog Post",
            excerpt="This is a test excerpt",
            content="This is test content for the blog post."
        )
        db.session.add(blog_post)
        
        # Add a test book
        book = Book(
            title="Test Book",
            author="Test Author",
            description="This is a test book description",
            age_range="Ages 13-18"
        )
        db.session.add(book)
        
        # Add a test video
        video = Video(
            title="Test Video",
            description="This is a test video description",
            youtube_id="test123",
            duration="5:00"
        )
        db.session.add(video)
        
        # Add a test survey response
        survey = Survey(
            age=16,
            financial_knowledge=3,
            games_rating=4,
            content_rating=4,
            favorite_topic="budgeting",
            suggestions="Test suggestion"
        )
        db.session.add(survey)
        
        db.session.commit()

    def test_home_page_loads(self):
        """Test that the home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'FinLit', response.data)
        self.assertIn(b'Master Your Money Skills', response.data)

    def test_games_page_loads(self):
        """Test that the games overview page loads successfully"""
        response = self.app.get('/games')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Financial Games', response.data)
        self.assertIn(b'Budget Challenge', response.data)
        self.assertIn(b'Saving Sprint', response.data)
        self.assertIn(b'Investment Sim', response.data)

    def test_individual_game_pages_load(self):
        """Test that individual game pages load successfully"""
        # Test Budget Challenge
        response = self.app.get('/games/budget')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Budget Challenge', response.data)
        
        # Test Saving Sprint
        response = self.app.get('/games/saving')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Saving Sprint', response.data)
        
        # Test Investment Simulation
        response = self.app.get('/games/invest')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Investment Simulation', response.data)

    def test_blog_list_loads(self):
        """Test that the blog list page loads successfully"""
        response = self.app.get('/blog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Financial Literacy Blog', response.data)
        self.assertIn(b'Test Blog Post', response.data)

    def test_blog_post_loads(self):
        """Test that individual blog posts load successfully"""
        response = self.app.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Blog Post', response.data)
        self.assertIn(b'This is test content', response.data)

    def test_books_page_loads(self):
        """Test that the books page loads successfully"""
        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Corner', response.data)
        self.assertIn(b'Test Book', response.data)

    def test_videos_page_loads(self):
        """Test that the videos page loads successfully"""
        response = self.app.get('/videos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Video Library', response.data)
        self.assertIn(b'Test Video', response.data)

    def test_survey_page_loads(self):
        """Test that the survey page loads successfully"""
        response = self.app.get('/survey')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'We Want Your Feedback', response.data)
        self.assertIn(b'How old are you', response.data)

    def test_survey_submission(self):
        """Test that survey submission works"""
        survey_data = {
            'age': '17',
            'financial_knowledge': '3',
            'games_rating': '4',
            'content_rating': '5',
            'favorite_topic': 'investing',
            'suggestions': 'Great app!'
        }
        
        response = self.app.post('/survey', data=survey_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your feedback', response.data)

    def test_budget_game_api(self):
        """Test that the budget game API works"""
        game_data = {
            'income': 900,
            'expenses': {
                'phone': 50,
                'transport': 60,
                'lunch': 80,
                'clothing': 40,
                'entertainment': 100,
                'shopping': 80,
                'eating_out': 70,
                'subscriptions': 30
            }
        }
        
        response = self.app.post('/api/games/budget', 
                               json=game_data,
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that response has expected fields
        self.assertIn('score', data)
        self.assertIn('savings', data)
        self.assertIn('savings_rate', data)
        self.assertIn('message', data)
        
        # Check that savings calculation is correct
        expected_savings = 900 - sum(game_data['expenses'].values())
        self.assertEqual(data['savings'], expected_savings)

    def test_investment_game_api(self):
        """Test that the investment game API works"""
        game_data = {
            'type': 'index',
            'amount': 1000,
            'years': 5
        }
        
        response = self.app.post('/api/games/invest',
                               json=game_data,
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check that response has expected fields
        self.assertIn('final_value', data)
        self.assertIn('total_return', data)
        self.assertIn('return_rate', data)
        self.assertIn('annual_returns', data)
        self.assertIn('explanation', data)
        
        # Check that final value is greater than initial amount (should grow over time)
        self.assertGreater(data['final_value'], game_data['amount'])

    def test_admin_access_protection(self):
        """Test that admin pages require access code"""
        response = self.app.get('/admin/survey-results')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Access Required', response.data)

    def test_admin_access_with_code(self):
        """Test that admin pages work with correct access code"""
        response = self.app.get('/admin/survey-results?code=admin123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Survey Results Dashboard', response.data)

    def test_404_error_handling(self):
        """Test that 404 errors are handled gracefully"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

    def test_invalid_blog_post_404(self):
        """Test that invalid blog post IDs return 404"""
        response = self.app.get('/blog/999')
        self.assertEqual(response.status_code, 404)

    def test_database_models(self):
        """Test that database models work correctly"""
        with app.app_context():
            # Test that we can query the models
            blog_posts = BlogPost.query.all()
            self.assertGreater(len(blog_posts), 0)
            
            books = Book.query.all()
            self.assertGreater(len(books), 0)
            
            videos = Video.query.all()
            self.assertGreater(len(videos), 0)
            
            surveys = Survey.query.all()
            self.assertGreater(len(surveys), 0)

    def test_static_files_structure(self):
        """Test that static files are accessible"""
        # Test CSS file
        response = self.app.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        
        # Test JS file
        response = self.app.get('/static/js/games.js')
        self.assertEqual(response.status_code, 200)

class FinLitIntegrationTests(unittest.TestCase):
    """Integration tests for more complex workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_complete_user_journey(self):
        """Test a complete user journey through the app"""
        # Start at home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Navigate to games
        response = self.app.get('/games')
        self.assertEqual(response.status_code, 200)
        
        # Try budget game
        response = self.app.get('/games/budget')
        self.assertEqual(response.status_code, 200)
        
        # Play budget game via API
        game_data = {
            'income': 800,
            'expenses': {
                'phone': 40,
                'transport': 50,
                'lunch': 60,
                'clothing': 30,
                'entertainment': 80,
                'shopping': 60,
                'eating_out': 50,
                'subscriptions': 20
            }
        }
        
        response = self.app.post('/api/games/budget', 
                               json=game_data,
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Submit feedback
        survey_data = {
            'age': '16',
            'financial_knowledge': '2',
            'games_rating': '5',
            'content_rating': '4',
            'favorite_topic': 'budgeting',
            'suggestions': 'Love the games!'
        }
        
        response = self.app.post('/survey', data=survey_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission

def run_tests():
    """Run all tests and display results"""
    print("Running FinLit Smoke Tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add smoke tests
    suite.addTest(unittest.makeSuite(FinLitSmokeTests))
    suite.addTest(unittest.makeSuite(FinLitIntegrationTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nResult: {'PASS' if success else 'FAIL'}")
    
    return success

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)