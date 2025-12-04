from django.shortcuts import render

# Homepage
def index(request):
    return render(request, 'index.html')

# About Page
def about(request):
    return render(request, 'about.html')

# Report a Conflict Page
def report(request):
    return render(request, 'report.html')

# View All Cases
def cases(request):
    return render(request, 'cases.html')

# Contact Page
def contact(request):
    return render(request, 'contact.html')



def analyze_report_text(text):
    text_lower = text.lower()

    # --- KEYWORDS ---
    danger_keywords = [
        'violence', 'attack', 'shooting', 'riot', 'killed', 'corruption',
        'fight', 'abuse', 'threat', 'crime', 'harassment', 'bomb'
    ]

    detected = [word for word in danger_keywords if word in text_lower]

    # --- SEVERITY ---
    if any(word in text_lower for word in ['killed', 'bomb', 'shooting', 'riot']):
        severity = "HIGH"
    elif any(word in text_lower for word in ['fight', 'threat', 'harassment']):
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # --- SUMMARY ---
    summary = text[:120] + "..." if len(text) > 120 else text

    return severity, summary, ", ".join(detected)
