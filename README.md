RnDTestProject
Assignment Instructions

Fork this GitHub repository and add MGsolutions-dev as a collaborator to complete the assignment.

Later, when submitting your application documents, you must provide the link to your forked GitHub repository.

Warning! If you do not provide a GitHub repository link, your application will be automatically rejected.

Assignment Description

“Analyze the given data based on NASM standards.”

The purpose is to evaluate whether you can estimate meaningful values from noisy data in order to assess a subject according to the NASM Overhead Squat Assessment.

Assignment Scenario

You are given movement data from 5 subjects, extracted using a 3D Motion Capture system.

However, due to sensor errors, the coordinate values contain significant noise.

Filter the data in a way that does not distort the key characteristics needed for evaluation, and assess each subject using the NASM Overhead Squat Assessment criteria.

Requirements
NASM-Based Overhead Squat Assessment

Using the provided data, evaluate the following items from the NASM Overhead Squat Assessment:

Anterior View

Knees moving inward or outward

Output the rotation angle of the knees

Lateral View

Low back arch

Output the degree of lumbar curvature

Torso leaning forward

Output the degree of torso forward lean

Deliverables

A results report

A document explaining the algorithm

Python-based project code and any unit test code used during development


python .\client.py
(.venv) PS C:\Users\e.bayaraa\Documents\datalab\agent\backend> python .\client.py 
Show generated SQL and agent debug details? [Y/n]: Y
Chat session started. Type /exit or /quit to end, /reset to start a new session.

You > 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

→ POST http://localhost:8000/api/v1/chat/analyze-debug
  session : [new]
  horizon : [server default]
  question: 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

[error] Could not reach http://localhost:8000/api/v1/chat/analyze-debug. Is the backend running?

You > 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

→ POST http://localhost:8000/api/v1/chat/analyze-debug
  session : [new]
  horizon : [server default]
  question: 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

[error] Could not reach http://localhost:8000/api/v1/chat/analyze-debug. Is the backend running?
                                                         
You > 
You > 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

→ POST http://localhost:8000/api/v1/chat/analyze-debug
  session : [new]
  horizon : [server default]
  question: 2025 оны хамгийн өндөр ашигт ажиллагаатай компани

Response status: 200
========================================================================
DEBUG: GENERATED SQL QUERY
========================================================================
SELECT symbol, companyname, netmargin, netprofit, revenue, year
FROM bdc_report_calculation
WHERE year = 2025
  AND netmargin IS NOT NULL
ORDER BY netmargin DESC
LIMIT 1

Query Parameters:
{}

========================================================================
DEBUG: Orchestration Decision
========================================================================
{
  "orchestration_signal": "data",
  "should_run_query": true,
  "data_requirements": [
    "revenue",
    "netprofit",
    "roa",
    "roe",
    "grossmargin",
    "netmargin",
    "ebitmargin",
    "totalpayable",
    "debtratio",
    "debttoequityratio",
    "financialleverage"
  ],
  "reason": "Financial data needed; send message to QueryAgent with required fields.",
  "start_year": 2025,
  "end_year": 2025,
  "summarize_earnings_call": false,
  "plain_english_for_teen": false
}

========================================================================
  N/A  |  source years: [2025]
========================================================================
# Монгол нэхмэл (MNH) – 2025 оны санхүүгийн үзүүлэлт

## Үндсэн дүнгээ

FY2025 санаа: MNH нь **цэвэр ашигт ажиллагааны түвшин 46.85%** бүхий сайн үйл ажиллагаа явуулж байна. Цэвэр ашиг **224.2 сая MNT** байгаа.

| Үзүүлэлт | Үнэ | Сэтгэгдэл |
|---------|-----|---------|
| Орлого (FY2025) | 4,786.0 сая MNT | Үндсэн үйл ажиллагаа |
| Цэвэр ашигт ажиллагаа | 46.85% | Өндөр (⚠️ нэмэлт баланс, үйл ажиллагааны зардал алга) |
| Цэвэр ашиг | 224.2 сая MNT | Цэвэр ашигт ажиллагаа × Орлого |

## Сэтгэгдэл

MNH-ийн цэвэр ашигт ажиллагааны түвшин 46.85% нь **өндөр** гэж үзэгдэж байгаа. Гэвч энэ дүнгээр өндөр үнэлгээ өгөхөөс өмнө дараахь хязгаарлалтуудыг тэмдэглэе:

1.
========================================================================

You > 
Session ended.

