from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Report

# --- Homepage ---
def index(request):
    return render(request, 'index.html')


# --- About Page ---
def about(request):
    return render(request, 'about.html')


# --- Report Conflict Page ---
def report_view(request):
    if request.method == "POST":
        # Collect form data
        region = request.POST.get("region")
        county = request.POST.get("county")
        case_type = request.POST.get("case_type")
        description = request.POST.get("description")
        anonymous = request.POST.get("anonymous") == "on"
        image = request.FILES.get("image")

        # Analyze text for severity, summary, and keywords
        severity, summary, keywords = analyze_report_text(description)

        # Save report
        report = Report(
            region=region,
            county=county,
            case_type=case_type,
            description=description,
            anonymous=anonymous,
            severity=severity,
            summary=summary,
            keywords=keywords
        )
        if image:
            report.image = image
        report.save()

        # Send email notification to admin
        try:
            send_mail(
                subject=f"New Conflict Report ({severity})",
                message=f"""
A new report has been submitted.

Type: {case_type}
Region: {region}
County: {county}
Severity: {severity}
Keywords: {keywords}
Anonymous: {'Yes' if anonymous else 'No'}

Description:
{description}
""",
                from_email="yourgmail@gmail.com",  # Replace with your email
                recipient_list=["yourgmail@gmail.com"],  # Replace with admin email
                fail_silently=False,
            )
        except Exception as e:
            print("Email failed:", e)

        messages.success(request, "Your report has been submitted successfully!")
        return redirect("report_success")

    return render(request, "report.html")


# --- Report Success Page ---
def report_success_view(request):
    return render(request, "report_success.html")


# --- View All Cases with Filters & Pagination ---
def cases(request):
    # Filters from GET parameters
    severity_filter = request.GET.get('severity')
    region_filter = request.GET.get('region')
    county_filter = request.GET.get('county')

    # Fetch reports ordered by latest first
    reports = Report.objects.order_by('-date_submitted')

    # Apply filters if selected
    if severity_filter:
        reports = reports.filter(severity=severity_filter)
    if region_filter:
        reports = reports.filter(region__iexact=region_filter)
    if county_filter:
        reports = reports.filter(county__iexact=county_filter)

    # Remove duplicates (based on case_type + region + county)
    seen = set()
    unique_reports = []
    for report in reports:
        key = (report.case_type, report.region, report.county)
        if key not in seen:
            unique_reports.append(report)
            seen.add(key)

    # Pagination: 6 reports per page
    paginator = Paginator(unique_reports, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Filter dropdown options (alphabetically)
    regions = sorted(Report.objects.values_list('region', flat=True).distinct())
    counties = sorted(Report.objects.values_list('county', flat=True).distinct())

    context = {
        "page_obj": page_obj,
        "regions": regions,
        "counties": counties,
        "selected_severity": severity_filter,
        "selected_region": region_filter,
        "selected_county": county_filter,
    }

    return render(request, "cases.html", context)


# --- Contact Page ---
def contact(request):
    return render(request, "contact.html")


# --- TEXT ANALYSIS FUNCTION ---
def analyze_report_text(text: str):
    """
    Analyze the report description to:
    - Detect keywords,
    - Determine severity (LOW, MEDIUM, HIGH),
    - Generate a summary (max 120 characters).
    """
    text_lower = text.lower()

    # Keywords to detect
    danger_keywords = [
        'violence', 'attack', 'shooting', 'riot', 'killed', 'corruption',
        'fight', 'abuse', 'threat', 'crime', 'harassment', 'bomb'
    ]
    detected_keywords = [word for word in danger_keywords if word in text_lower]

    # Determine severity
    if any(word in text_lower for word in ['killed', 'bomb', 'shooting', 'riot']):
        severity = "HIGH"
    elif any(word in text_lower for word in ['fight', 'threat', 'harassment']):
        severity = "MEDIUM"
    else:
        severity = "LOW"

    # Generate summary (max 120 characters)
    summary = text[:120] + "..." if len(text) > 120 else text

    return severity, summary, ", ".join(detected_keywords)
