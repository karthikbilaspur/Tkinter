import tkinter as tk
from tkinter import messagebox
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3
import hashlib
import logging
import os

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

class SentimentDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(background="light green")
        self.root.title("Sentiment Detector")
        self.root.geometry("300x400")

        self.create_widgets()

        # Create a database connection
        self.conn = sqlite3.connect("sentiment_analysis.db")
        self.cursor = self.conn.cursor()

        # Create a table to store sentiment analysis results
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY,
                text TEXT,
                sentiment TEXT,
                sentiment_score REAL
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Create label and text area
        self.label = tk.Label(self.root, text="Enter Your Sentence", bg="light green")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.text_area = tk.Text(self.root, height=5, width=25, font="lucida 13")
        self.text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create buttons
        self.check_button = tk.Button(self.root, text="Check Sentiment", fg="Black", bg="Red", command=self.detect_sentiment)
        self.check_button.grid(row=2, column=0, padx=10, pady=10)

        self.clear_button = tk.Button(self.root, text="Clear", fg="Black", bg="Red", command=self.clear_all)
        self.clear_button.grid(row=2, column=1, padx=10, pady=10)

        self.view_button = tk.Button(self.root, text="View Results", fg="Black", bg="Red", command=self.view_results)
        self.view_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", fg="Black", bg="Red", command=self.root.destroy)
        self.exit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Create labels and entry fields for sentiment scores
        self.negative_label = tk.Label(self.root, text="Negative:", bg="light green")
        self.negative_label.grid(row=5, column=0, padx=10, pady=10)

        self.negative_field = tk.Entry(self.root, width=25)
        self.negative_field.grid(row=5, column=1, padx=10, pady=10)

        self.neutral_label = tk.Label(self.root, text="Neutral:", bg="light green")
        self.neutral_label.grid(row=6, column=0, padx=10, pady=10)

        self.neutral_field = tk.Entry(self.root, width=25)
        self.neutral_field.grid(row=6, column=1, padx=10, pady=10)

        self.positive_label = tk.Label(self.root, text="Positive:", bg="light green")
        self.positive_label.grid(row=7, column=0, padx=10, pady=10)

        self.positive_field = tk.Entry(self.root, width=25)
        self.positive_field.grid(row=7, column=1, padx=10, pady=10)

        self.overall_label = tk.Label(self.root, text="Overall Sentiment:", bg="light green")
        self.overall_label.grid(row=8, column=0, padx=10, pady=10)

        self.overall_field = tk.Entry(self.root, width=25)
        self.overall_field.grid(row=8, column=1, padx=10, pady=10)

    def detect_sentiment(self):
        try:
            # Get text from text area
            text = self.text_area.get("1.0", "end")

            # Create a SentimentIntensityAnalyzer object
            sia = SentimentIntensityAnalyzer()

            # Get sentiment scores
            sentiment_scores = sia.polarity_scores(text)

            # Clear entry fields
            self.clear_all()

            # Insert sentiment scores into entry fields
            self.negative_field.insert(0, f"{sentiment_scores['neg']*100}% Negative")
            self.neutral_field.insert(0, f"{sentiment_scores['neu']*100}% Neutral")
            self.positive_field.insert(0, f"{sentiment_scores['pos']*100}% Positive")

            # Determine overall sentiment
            if sentiment_scores['compound'] >= 0.05:
                overall_sentiment = "Positive"
            elif sentiment_scores['compound'] <= -0.05:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"

            # Insert overall sentiment into entry field
            self.overall_field.insert(0, overall_sentiment)

            # Hash text using SHA-256
            text_hash = hashlib.sha256(text.encode()).hexdigest()

            # Store sentiment analysis results in the database
            self.cursor.execute("""
                INSERT INTO sentiment_analysis (text_hash, text, sentiment, sentiment_score)
                VALUES (?, ?, ?, ?)
            """, (text_hash, text, overall_sentiment, sentiment_scores['compound']))
            self.conn.commit()

            logging.info(f"Sentiment analysis results stored in database: {text_hash}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error occurred during sentiment analysis: {str(e)}")

    def clear_all(self):
        # Clear text area and entry fields
        self.text_area.delete("1.0", "end")
        self.negative_field.delete(0, "end")
        self.neutral_field.delete(0, "end")
        self.positive_field.delete(0, "end")
        self.overall_field.delete(0, "end")

    def view_results(self):
        # Create a new window to display sentiment analysis results
        results_window = tk.Toplevel(self.root)
        results_window.title("Sentiment Analysis Results")

        # Create a text box to display results
        results_text = tk.Text(results_window, height=10, width=40)
        results_text.pack(padx=10, pady=10)

        # Retrieve sentiment analysis results from the database
        self.cursor.execute("SELECT * FROM sentiment_analysis")
        results = self.cursor.fetchall()

        # Display results in the text box
        for result in results:
            results_text.insert(tk.END, f"Text Hash: {result[0]}\nText: {result[1]}\nSentiment: {result[2]}\nSentiment Score: {result[3]}\n\n")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SentimentDetector()
    app.run()