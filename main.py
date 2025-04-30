import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

# Apply modern Matplotlib style
plt.style.use('ggplot')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.work_btn.clicked.connect(self.show_work_page)
        self.career_btn.clicked.connect(self.show_career_page)
        self.land_btn.clicked.connect(self.show_land_page)
        self.dev_btn.clicked.connect(self.load_dev_chart)

   
        self.df = pd.read_csv("result.csv")


        fig = Figure(figsize=(12, 8))
        canvas = FigureCanvas(fig)
        self.create_age_chart(fig, self.df)
        self.create_framework_chart(self.df)
        self.create_scatter_plot(self.df)
        self.create_scatter_plot_sal(self.df)
        self.create_education_chart(fig, self.df)
        fig.tight_layout()

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.chart.setLayout(layout)
        self.chart.setStyleSheet("border: none;")

        self.lang_chart_loaded = False  

    def create_age_chart(self, fig, df):
        age_counts = df['Age'].value_counts().reindex([
            'Under 18 years old',
            '18-24 years old',
            '25-34 years old',
            '35-44 years old',
            '45-54 years old',
            '55-64 years old',
            '65 years or older',
            'Prefer not to say'
        ])
        sizes = age_counts.dropna()
        percentages = (sizes / sizes.sum() * 100).round(1)

        ax = fig.add_subplot(211)
        colors = ['#5d9cec', '#e86a5c', '#a3cc72', '#f5a742', '#65c3ba', '#9370db', '#e37fb7', '#f4e87d']
        bars = ax.barh(sizes.index, percentages, color=colors, height=0.7, edgecolor='white', linewidth=1.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold')
        ax.set_title("Age Group Distribution", fontsize=16, weight='bold', pad=20)
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

    def create_education_chart(self, fig, df):
        education_order = [
            'Primary/elementary school',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)',
            'Some college/university study without earning a degree',
            'Associate degree (A.A., A.S., etc.)',
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
            'Professional degree (JD, MD, Ph.D, Ed.D, etc.)',
            'Something else'
        ]
        ed_counts = df['EdLevel'].value_counts().reindex(education_order)
        ed_percentages = (ed_counts / ed_counts.sum() * 100).round(1)
        ax = fig.add_subplot(212)

        short_labels = {
            'Primary/elementary school': 'Primary',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Secondary',
            'Some college/university study without earning a degree': 'Some college',
            'Associate degree (A.A., A.S., etc.)': 'Associate',
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's",
            'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Professional',
            'Something else': 'Other'
        }

        display_labels = [short_labels.get(label, label) for label in ed_counts.index]
        ed_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633', '#00b3b3', '#9933cc', '#333333']
        bars = ax.barh(display_labels, ed_percentages, color=ed_colors, height=0.7, edgecolor='white', linewidth=1.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold')
        ax.set_title("Education Level Distribution", fontsize=16, weight='bold', pad=20)
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

    def create_language_chart(self, df):
       
        all_langs = [lang for langs in df['LanguageHaveWorkedWith'].dropna().str.split(';') for lang in langs]
        lang_series = pd.Series(all_langs).value_counts()
        top_7 = lang_series.head(7)
        percentages = (top_7 / top_7.sum() * 100).round(1)


        fig = Figure(figsize=(7, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        colors = plt.cm.tab10.colors
        bars = ax.barh(top_7.index[::-1], percentages[::-1], color=colors, height=0.6, edgecolor='white', linewidth=1.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold')

        ax.set_title("Top 7 Languages Worked With", fontsize=15, weight='bold', pad=15)
        ax.set_xlabel("Percentage (%)", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()


        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.dev_chart_container.setLayout(layout)
        self.dev_chart_container.setStyleSheet("border: none;")

    def load_dev_chart(self):
        self.show_dev_page()
        if not self.lang_chart_loaded:
            self.lang_chart_loaded = True
            self.create_language_chart(self.df)

    def show_work_page(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_career_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_land_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_dev_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def create_framework_chart(self, df):

        all_frames = [fw for frameworks in df['WebframeHaveWorkedWith'].dropna().str.split(';') for fw in frameworks]
        frame_series = pd.Series(all_frames).value_counts()
        top_7 = frame_series.head(7)
        percentages = (top_7 / top_7.sum() * 100).round(1)

   
        fig = Figure(figsize=(7, 5))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        colors = plt.cm.Pastel1.colors
        bars = ax.barh(top_7.index[::-1], percentages[::-1], color=colors, height=0.6, edgecolor='white', linewidth=1.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold')

        ax.set_title("Top 7 Web Frameworks", fontsize=15, weight='bold', pad=15)
        ax.set_xlabel("Percentage (%)", fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.fram_top.setLayout(layout)
        self.fram_top.setStyleSheet("border: none;")


    def create_scatter_plot_sal(self, df):
   
        scatter_df = df[['WorkExp', 'CompTotal']].dropna()

        scatter_df['WorkExp'] = pd.to_numeric(scatter_df['WorkExp'], errors='coerce')
        scatter_df['CompTotal'] = pd.to_numeric(scatter_df['CompTotal'], errors='coerce')
        scatter_df.dropna(inplace=True)

  
        scatter_df = scatter_df[(scatter_df['CompTotal'] < 500000) & (scatter_df['WorkExp'] < 50)]


        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)


        ax.scatter(scatter_df['WorkExp'], scatter_df['CompTotal'], alpha=0.5, color='#5dade2', edgecolors='w', linewidth=0.5)

        ax.set_title("Salary vs Experience", fontsize=16, weight='bold', pad=15)
        ax.set_xlabel("Years of Experience", fontsize=12)
        ax.set_ylabel("Total Compensation (USD)", fontsize=12)

        ax.grid(True, linestyle='--', alpha=0.6)
        fig.tight_layout()

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.scat_plt.setLayout(layout)
        self.scat_plt.setStyleSheet("border: none;")

    def create_scatter_plot(self, df):
    
        scatter_df = df[['WorkExp', 'JobSat']].dropna()

   
        scatter_df['WorkExp'] = pd.to_numeric(scatter_df['WorkExp'], errors='coerce')
        scatter_df['JobSat'] = pd.to_numeric(scatter_df['JobSat'], errors='coerce')
        scatter_df.dropna(inplace=True)

     
        scatter_df = scatter_df[(scatter_df['WorkExp'] < 50) & (scatter_df['JobSat'] <= 10)]

  
        fig = Figure(figsize=(8, 6))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)


        scatter = ax.scatter(
            scatter_df['WorkExp'],
            scatter_df['JobSat'],
            alpha=0.5,
            color='#58D68D',
            edgecolors='w',
            linewidth=0.5
        )


        ax.set_title("Experience vs Job Satisfaction", fontsize=16, weight='bold', pad=15)
        ax.set_xlabel("Years of Experience", fontsize=12)
        ax.set_ylabel("Job Satisfaction (1 = Low, 10 = High)", fontsize=12)


        ax.grid(True, linestyle='--', alpha=0.6)
        fig.tight_layout()


        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.scat_plt2.setLayout(layout)
        self.scat_plt2.setStyleSheet("border: none;")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
