import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.enum.chart import XL_TICK_MARK
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_VERTICAL_ANCHOR
import datetime


def make_slides(df, data_dict, file_name):
    # create presentation
    prs = Presentation()

    ### SLIDE FRONT ##############################################

    front = prs.slides.add_slide(prs.slide_layouts[6])
    # TEXTBOX
    textbox = front.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(2))
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    # Add text to the textbox
    p1 = text_frame.add_paragraph()
    p1.text = f"CyberMarket Simulation: {data_dict['scenarioName']}"
    p1.font.size = Pt(32)
    p1.font.color.rgb = RGBColor(16, 53, 117)
    p1.font.bold = True
    p1.alignment = 2

    p2 = text_frame.add_paragraph()
    my_time = datetime.datetime.now() + datetime.timedelta(hours=3)
    p2.text = f"{my_time.strftime("%Y-%m-%d %H:%M:%S")}"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(16, 53, 117)
    p2.font.bold = True
    p2.alignment = 2

    ### SLIDE 1 ##############################################
    # Scenario assumptions

    slide1 = prs.slides.add_slide(prs.slide_layouts[6])

    # TEXTBOX
    textbox = slide1.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9.5), Inches(3))
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    # Add text to the textbox
    p1 = text_frame.add_paragraph()
    p1.text = "Main Scenario Assumptions:"
    p1.font.size = Pt(28)
    p1.font.color.rgb = RGBColor(16, 53, 117)
    p1.font.bold = True
    p1.alignment = 1
    # Policy price
    p2 = text_frame.add_paragraph()
    p2.text = f'Policy Price: ₪{data_dict['insurancePrice']:,.0f}'
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(16, 53, 117)
    p2.alignment = 1
    # Commission Rates
    p3 = text_frame.add_paragraph()
    p3.text = (f'Commission Rates: New: {data_dict['newCommission']:.0f}%, Referred: {data_dict['referredCommission']:.0f}%, '
               f'Lead: {data_dict['leadCommission']:.0f}%, Existing: {data_dict['existingCommission']:.0f}%')
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(16, 53, 117)
    p3.alignment = 1
    # Cyber Services Commission
    p4 = text_frame.add_paragraph()
    p4.text = f'Cyber Commission: ₪ per service policy'
    p4.font.size = Pt(18)
    p4.font.color.rgb = RGBColor(16, 53, 117)
    p4.alignment = 1
    # Service Times
    p5 = text_frame.add_paragraph()
    p5.text = (f'Service Times: Schedule meeting:  min., Sales meeting:  min., '
               f'Cyber analysis:  min.')
    p5.font.size = Pt(18)
    p5.font.color.rgb = RGBColor(16, 53, 117)
    p5.alignment = 1
    # Salaries
    p6 = text_frame.add_paragraph()
    p6.text = (f'Salaries: Admin: ₪{data_dict['adminSalary']:,.0f}, Tele meeting: ₪{data_dict['teleSalary']:,.0f}, '
               f'Sales: ₪{data_dict['salesSalary']:,.0f}, Analyst: ₪{data_dict['cyberSalary']:,.0f}, '
               f'Logistics: ₪{data_dict['logisticsSalary']:,.0f}')
    p6.font.size = Pt(16)
    p6.font.color.rgb = RGBColor(16, 53, 117)
    p6.alignment = 1
    # Incentives
    p7 = text_frame.add_paragraph()
    p7.text = (f'Bonuses: Schedule Sales Meeting: ₪{data_dict['teleIncentive']:,.0f}, '
               f'Policy Sale: {data_dict['salesIncentive']:.0f}% of commission')
    p7.font.size = Pt(16)
    p7.font.color.rgb = RGBColor(16, 53, 117)
    p7.alignment = 1
    # Cost of Lead (buying Policy)
    p8 = text_frame.add_paragraph()
    p8.text = (f' Cost of lead: ₪')
    p8.font.size = Pt(18)
    p8.font.color.rgb = RGBColor(16, 53, 117)
    p8.alignment = 1
    # Perceived risk
    p9 = text_frame.add_paragraph()
    p9.text = (
        f'Risk Perception: New: {data_dict['newRisk']:.0f}%, Referred: {data_dict['referredRisk']:.0f}%, '
        f'Lead: {data_dict['leadRisk']:.0f}%, Existing: {data_dict['existingRisk']:.0f}%')
    p9.font.size = Pt(18)
    p9.font.color.rgb = RGBColor(16, 53, 117)
    p9.alignment = 1

    # Set the line spacing
    for p in text_frame.paragraphs:
        p.line_spacing = 2

    # Save the presentation to the given file path
    prs.save(file_name)