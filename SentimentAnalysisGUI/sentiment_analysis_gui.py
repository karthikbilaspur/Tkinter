from tkinter import *
from tkinter import messagebox
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentDetector:
    def __init__(self):
        self.root = Tk()
        self.root.config(background="light green")
        self.root.title("Sentiment Detector")
        self.root.geometry("300x400")

        self.create_widgets()

    def create_widgets(self):
        # Create label and text area
        self.label = Label(self.root, text="Enter Your Sentence", bg="light green")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.text_area = Text(self.root, height=5, width=25, font="lucida 13")
        self.text_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create buttons
        self.check_button = Button(self.root, text="Check Sentiment", fg="Black", bg="Red", command=self.detect_sentiment)
        self.check_button.grid(row=2, column=0, padx=10, pady=10)

        self.clear_button = Button(self.root, text="Clear", fg="Black", bg="Red", command=self.clear_all)
        self.clear_button.grid(row=2, column=1, padx=10, pady=10)

        self.exit_button = Button(self.root, text="Exit", fg="Black", bg="Red", command=self.root.destroy)
        self.exit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Create labels and entry fields for sentiment scores
        self.negative_label = Label(self.root, text="Negative:", bg="light green")
        self.negative_label.grid(row=4, column=0, padx=10, pady=10)

        self.negative_field = Entry(self.root, width=25)
        self.negative_field.grid(row=4, column=1, padx=10, pady=10)

        self.neutral_label = Label(self.root, text="Neutral:", bg="light green")
        self.neutral_label.grid(row=5, column=0, padx=10, pady=10)

        self.neutral_field = Entry(self.root, width=25)
        self.neutral_field.grid(row=5, column=1, padx=10, pady=10)

        self.positive_label = Label(self.root, text="Positive:", bg="light green")
        self.positive_label.grid(row=6, column=0, padx=10, pady=10)

        self.positive_field = Entry(self.root, width=25)
        self.positive_field.grid(row=6, column=1, padx=10, pady=10)

        self.overall_label = Label(self.root, text="Overall Sentiment:", bg="light green")
        self.overall_label.grid(row=7, column=0, padx=10, pady=10)

        self.overall_field = Entry(self.root, width=25)
        self.overall_field.grid(row=7, column=1, padx=10, pady=10)

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
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_all(self):
        # Clear text area and entry fields
        self.text_area.delete("1.0", "end")
        self.negative_field.delete(0, "end")
        self.neutral_field.delete(0, "end")
        self.positive_field.delete(0, "end")
        self.overall_field.delete(0, "end")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SentimentDetector()
    app.run()