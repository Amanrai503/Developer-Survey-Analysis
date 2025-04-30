import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect,QVBoxLayout
from PyQt5 import uic
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Stack_ui.ui', self) 
        self.setWindowTitle("Dashboard")
        self.apply_shadows_widget()


        self.df = pd.read_csv("result.csv")
        fig = Figure(figsize=(12, 8))
        self.create_education_chart(self.df)
        self.create_education_chart_pro(self.df)
        self.create_education_chart_learn(self.df)
        self.create_learncode_chart_for_devs(self.df)
        self.create_top_languages_chart_for_devs(self.df)
        self.create_experience_chart(self.df)
        self.create_top_languages_chart_for_devs_learning(self.df)
        self.create_top_database_chart_for_devs(self.df)

        self.create_top_cloud_platforms_chart_for_devs(self.df)



        self.dev_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.tech_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))



        self.all_btn_2.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(0))
        self.learn_btn_2.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(1))


        self.all_btn.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.pro_btn.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))
        self.learn_btn.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(2))


    def apply_shadows_widget(self):
        frames = [self.tab_holder,self.widget_3,self.widget_5,self.widget_7 ]
        for frame in frames:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setOffset(2, 6)
            shadow.setColor(QColor(192, 192, 192))  #(37, 33, 56)  #(204, 204, 204)
            frame.setGraphicsEffect(shadow)

    
    def create_education_chart(self, df):
        # Create a new figur
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        if self.edu_wid.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self.edu_wid.setLayout(layout)
        self.edu_wid.layout().addWidget(canvas)

        # Chart code
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
        ax = fig.add_subplot(111)

        short_labels = {
            'Primary/elementary school': 'Primary',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Secondary',
            'Some college/university study without earning a degree': 'Some college',
            'Associate degree (A.A., A.S., etc.)': 'Associate degree',
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
            'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Professional degree',
            'Something else': 'Other'
        }

        display_labels = [short_labels.get(label, label) for label in ed_counts.index]
        ed_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633', '#00b3b3', '#9933cc', '#333333']
        bars = ax.barh(display_labels, ed_percentages, color=ed_colors, height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold', color='white')

        ax.set_title("Education Level Distribution", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()


    def create_education_chart_pro(self, df):
        # Filter for professional developers only
        dev_df = df[df['MainBranch'] == "I am a developer by profession"]

        # Create a new figure with same styling
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.pro_wid.layout().addWidget(canvas)

        # Define order of education levels
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

        # Calculate percentages from devs only
        ed_counts = dev_df['EdLevel'].value_counts().reindex(education_order)
        ed_percentages = (ed_counts / ed_counts.sum() * 100).round(1)

        # Axis and labels
        ax = fig.add_subplot(111)
        short_labels = {
            'Primary/elementary school': 'Primary',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Secondary',
            'Some college/university study without earning a degree': 'Some college',
            'Associate degree (A.A., A.S., etc.)': 'Associate degree',
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
            'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Professional degree',
            'Something else': 'Other'
        }
        display_labels = [short_labels.get(label, label) for label in ed_counts.index]

        ed_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633', '#00b3b3', '#9933cc', '#333333']
        bars = ax.barh(display_labels, ed_percentages, color=ed_colors, height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold', color='white')

        # Match styling exactly
        ax.set_title("Education Level (Professional Developers)", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        fig.tight_layout()

    def create_education_chart_learn(self, df):
        # Filter for professional developers only
        dev_df = df[df['MainBranch'] == "I am learning to code"]

        # Create a new figure with same styling
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.learn_wid.layout().addWidget(canvas)

        # Define order of education levels
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

        # Calculate percentages from devs only
        ed_counts = dev_df['EdLevel'].value_counts().reindex(education_order)
        ed_percentages = (ed_counts / ed_counts.sum() * 100).round(1)

        # Axis and labels
        ax = fig.add_subplot(111)
        short_labels = {
            'Primary/elementary school': 'Primary',
            'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)': 'Secondary',
            'Some college/university study without earning a degree': 'Some college',
            'Associate degree (A.A., A.S., etc.)': 'Associate degree',
            "Bachelor’s degree (B.A., B.S., B.Eng., etc.)": "Bachelor's degree",
            "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)": "Master's degree",
            'Professional degree (JD, MD, Ph.D, Ed.D, etc.)': 'Professional degree',
            'Something else': 'Other'
        }
        display_labels = [short_labels.get(label, label) for label in ed_counts.index]

        ed_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633', '#00b3b3', '#9933cc', '#333333']
        bars = ax.barh(display_labels, ed_percentages, color=ed_colors, height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold', color='white')

        # Match styling exactly
        ax.set_title("Education Level (Professional Developers)", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)

        fig.tight_layout()


    def create_learncode_chart_for_devs(self, df):
        from collections import defaultdict

        # Drop missing values and get valid responses
        df_valid = df[['LearnCode']].dropna()
        total_respondents = df_valid.shape[0]

        # Initialize method-to-count mapping
        method_counts = defaultdict(int)

        # Count how many respondents selected each method
        for methods in df_valid['LearnCode']:
            selected = set(m.strip() for m in methods.split(';'))  # Use set to avoid double-counting
            for method in selected:
                method_counts[method] += 1

        # Define desired order and short labels
        desired_order = [
            'Other online resources (e.g., videos, blogs, forum, online community)',
            'Books / Physical media',
            'Online Courses or Certification',
            'School (i.e., University, College, etc)',
            'On the job training',
            'Colleague',
            'Coding Bootcamp',
            'Friend or family member'
        ]

        short_labels = {
            'Books / Physical media': 'Books / Physical media',
            'Coding Bootcamp': 'Coding Bootcamp',
            'Colleague': 'Colleague',
            'Friend or family member': 'Friend or family member',
            'Online Courses or Certification': 'E-courses or Certification',
            'On the job training': 'On the job training',
            'Other online resources (e.g., videos, blogs, forum, online community)': 'Other online resources',
            'School (i.e., University, College, etc)': 'School'
        }

        # Calculate percentages based on total respondents
        percentages = {
            short_labels[k]: round(method_counts[k] / total_respondents * 100, 1)
            for k in desired_order if k in method_counts
        }

        # Plotting
        fig = Figure(facecolor='#3b4045')  # Background color
        canvas = FigureCanvas(fig)
        self.edu_wid_2.layout().addWidget(canvas)

        ax = fig.add_subplot(111)
        labels = list(percentages.keys())
        values = list(percentages.values())

        bar_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633', '#00b3b3', '#9933cc', '#333333']

        bars = ax.barh(labels, values, color=bar_colors[:len(labels)], height=0.7, edgecolor='white', linewidth=1.5)
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold', color='white')

        ax.set_title("How Developers Learned to Code", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()


    def create_top_database_chart_for_devs(self, df):

        # Filter for developers learning to code
        #df = df[df['MainBranch'] == 'I am learning to code']

        # Drop missing values and split selections
        db_series = df['DatabaseWantToWorkWith'].dropna().str.split(';')
        flat_list = [db.strip() for sublist in db_series for db in sublist]

        # Count occurrences
        counts = Counter(flat_list)

        # Specified order
        custom_order = [
            'PostgreSQL', 'MySQL', 'SQLite', 'Microsoft SQL Server', 'MongoDB'
        ]

        # Filter and calculate percentages
        filtered_counts = {db: counts[db] for db in custom_order if db in counts}
        total_respondents = df['DatabaseWantToWorkWith'].dropna().shape[0]
        percentages = {db: round((count / total_respondents) * 100, 1) for db, count in filtered_counts.items()}

        # Short display labels
        short_labels = {
            'PostgreSQL': 'PostgreSQL',
            'MySQL': 'MySQL',
            'SQLite': 'SQLite',
            'Microsoft SQL Server': 'MS SQL',
            'MongoDB': 'MongoDB'
        }

        # Apply custom order to labels and values
        display_labels = [short_labels[db] for db in custom_order if db in percentages]
        values = [percentages[db] for db in custom_order if db in percentages]

        # Color palette
        bar_colors = ['#e67300', '#3399ff', '#9966cc', '#cc3333', '#66cc66']

        # Chart setup
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.edu_wid_4.layout().addWidget(canvas)

        ax = fig.add_subplot(111)

        # Plot horizontal bar chart
        bars = ax.barh(display_labels, values, color=bar_colors[:len(display_labels)], height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left',
                    fontweight='bold', color='white')

        # Styling
        ax.set_title("Top Databases Among New Coders", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()



    def create_top_languages_chart_for_devs_learning(self, df):
        

        # Filter only those who are learning to code
        df = df[df['MainBranch'] == 'I am learning to code']

        # Drop missing values and split multiple selections
        lang_series = df['LanguageHaveWorkedWith'].dropna().str.split(';')
        flat_list = [lang.strip() for sublist in lang_series for lang in sublist]

        # Count occurrences
        counts = Counter(flat_list)

        # Your specified custom order
        custom_order = [
            'JavaScript', 'HTML/CSS', 'Python', 'SQL',
            'TypeScript', 'Bash/Shell (all shells)', 'Java',
            'C#', 'C++', 'C'
        ]

        # Filter and calculate percentages (based on number of respondents)
        filtered_counts = {lang: counts[lang] for lang in custom_order if lang in counts}
        total_respondents = df['LanguageHaveWorkedWith'].dropna().shape[0]
        percentages = {lang: round((count / total_respondents) * 100, 1) for lang, count in filtered_counts.items()}

        # Map to short display labels
        short_labels = {
            'JavaScript': 'JS',
            'HTML/CSS': 'HTML/CSS',
            'Python': 'PY',
            'SQL': 'SQL',
            'TypeScript': 'TS',
            'Bash/Shell (all shells)': 'Bash/Shell',
            'Java': 'Java',
            'C#': 'C#',
            'C++': 'C++',
            'C': 'C'
        }

        # Apply custom order to labels and values
        display_labels = [short_labels[lang] for lang in custom_order if lang in percentages]
        values = [percentages[lang] for lang in custom_order if lang in percentages]

        # Color palette
        bar_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633',
                    '#00b3b3', '#9933cc', '#ff6666', '#6699ff', '#33cc99']

        # Chart setup
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.pro_wid_2.layout().addWidget(canvas)

        ax = fig.add_subplot(111)

        # Plot horizontal bar chart
        bars = ax.barh(display_labels, values, color=bar_colors[:len(display_labels)], height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left',
                    fontweight='bold', color='white')

        # Styling
        ax.set_title("Top Languages Among New Coders", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()



    def create_top_languages_chart_for_devs(self, df):

        # Drop missing values and split multiple selections
        lang_series = df['LanguageHaveWorkedWith'].dropna().str.split(';')
        flat_list = [lang.strip() for sublist in lang_series for lang in sublist]

        # Count occurrences
        counts = Counter(flat_list)

        # Your specified custom order
        custom_order = [
            'JavaScript', 'HTML/CSS', 'Python', 'SQL',
            'TypeScript', 'Bash/Shell (all shells)', 'Java',
            'C#', 'C++', 'C'
        ]

        # Filter and calculate percentages (based on number of respondents)
        filtered_counts = {lang: counts[lang] for lang in custom_order if lang in counts}
        total_respondents = df['LanguageHaveWorkedWith'].dropna().shape[0]
        percentages = {lang: round((count / total_respondents) * 100, 1) for lang, count in filtered_counts.items()}

        # Map to short display labels
        short_labels = {
            'JavaScript': 'JS',
            'HTML/CSS': 'HTML/CSS',
            'Python': 'PY',
            'SQL': 'SQL',
            'TypeScript': 'TS',
            'Bash/Shell (all shells)': 'Bash/Shell',
            'Java': 'Java',
            'C#': 'C#',
            'C++': 'C++',
            'C': 'C'
        }

        # Apply custom order to labels and values
        display_labels = [short_labels[lang] for lang in custom_order if lang in percentages]
        values = [percentages[lang] for lang in custom_order if lang in percentages]

        # Color palette
        bar_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f', '#996633',
                    '#00b3b3', '#9933cc', '#ff6666', '#6699ff', '#33cc99']

        # Chart setup
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.pro_wid_3.layout().addWidget(canvas)

        ax = fig.add_subplot(111)

        # Plot horizontal bar chart
        bars = ax.barh(display_labels, values, color=bar_colors[:len(display_labels)], height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left',
                    fontweight='bold', color='white')

        # Styling
        ax.set_title("Top 10 Languages Used by Developers", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()


    def create_experience_chart(self, df):
        # Drop missing values
        years_series = df['YearsCodePro'].dropna()

        # Convert "Less than 1 year" to 0 and others to numeric
        def categorize_experience(value):
            if value == "Less than 1 year":
                return "Less than 1 year"
            try:
                years = float(value)
                if 1 <= years <= 4:
                    return "1 to 4"
                elif 5 <= years <= 9:
                    return "5 to 9"
                elif 10 <= years <= 14:
                    return "10 to 14"
                elif 15 <= years <= 19:
                    return "15 to 19"
                elif 20 <= years <= 24:
                    return "20 to 24"
                elif 25 <= years <= 29:
                    return "25 to 29"
                else:
                    return "30 and above"
            except:
                return None

        categorized = years_series.map(categorize_experience).dropna()

        # Count occurrences
        counts = Counter(categorized)

        # Define desired order
        category_order = [
            "Less than 1 year", "1 to 4", "5 to 9", "10 to 14",
            "15 to 19", "20 to 24", "25 to 29", "30 and above"
        ]
        ordered_counts = {cat: counts.get(cat, 0) for cat in category_order}

        total = sum(ordered_counts.values())
        percentages = {k: round(v / total * 100, 1) for k, v in ordered_counts.items()}

        # Create chart
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.exp_code.layout().addWidget(canvas)

        ax = fig.add_subplot(111)
        labels = list(percentages.keys())
        values = list(percentages.values())

        # Color palette for consistency
        bar_colors = ['#5cb85c', '#337ab7', '#f0ad4e', '#d9534f',
                    '#996633', '#00b3b3', '#9933cc', '#333333']

        bars = ax.barh(labels, values, color=bar_colors, height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left', fontweight='bold', color='white')

        # Chart styling
        ax.set_title("Years of Professional Coding Experience", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()


    def create_top_cloud_platforms_chart_for_devs(self, df):

        # Drop missing values and split selections
        cloud_series = df['PlatformHaveWorkedWith'].dropna().str.split(';')
        flat_list = [platform.strip() for sublist in cloud_series for platform in sublist]

        # Count occurrences
        counts = Counter(flat_list)

        # Specified order
        custom_order = [
            'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud', 'Cloudflare', 'Firebase'
        ]

        # Filter and calculate percentages
        filtered_counts = {platform: counts[platform] for platform in custom_order if platform in counts}
        total_respondents = df['PlatformHaveWorkedWith'].dropna().shape[0]
        percentages = {platform: round((count / total_respondents) * 100, 1) for platform, count in filtered_counts.items()}

        # Short display labels
        short_labels = {
            'Amazon Web Services (AWS)': 'AWS',
            'Microsoft Azure': 'Azure',
            'Google Cloud': 'GCP',
            'Cloudflare': 'Cloudflare',
            'Firebase': 'Firebase'
        }

        # Apply custom order to labels and values
        display_labels = [short_labels[platform] for platform in custom_order if platform in percentages]
        values = [percentages[platform] for platform in custom_order if platform in percentages]

        # Color palette (same style)
        bar_colors = ['#ff9933', '#6699ff', '#66cc99', '#cc6699', '#ff6666']

        # Chart setup
        fig = Figure(facecolor='#3b4045')
        canvas = FigureCanvas(fig)
        self.pro_wid_4.layout().addWidget(canvas)

        ax = fig.add_subplot(111)

        # Plot horizontal bar chart
        bars = ax.barh(display_labels, values, color=bar_colors[:len(display_labels)], height=0.7, edgecolor='white', linewidth=1.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{width}%', va='center', ha='left',
                    fontweight='bold', color='white')

        # Styling
        ax.set_title("Top Cloud Platforms Among New Coders", fontsize=16, weight='bold', pad=20, color='white')
        ax.set_xlabel("Percentage (%)", fontsize=12, labelpad=10, color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#3b4045')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        fig.tight_layout()



def main():
    app = QApplication(sys.argv)  
    window = MainWindow()       
    window.show()                 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()