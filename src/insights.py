
from collections import Counter
from datetime import datetime
from src.summarizer import FormSummarizer

class MultiFormInsights:
    def __init__(self):
        self.summarizer = FormSummarizer()

    def process_forms(self, extracted_fields_list: list) -> dict:
        
        all_names = []
        all_dobs = []
        all_addresses = []

        for fields in extracted_fields_list:
            if fields.get("name"):
                all_names.append(fields["name"])
            if fields.get("dob"):
                all_dobs.append(fields["dob"])
            if fields.get("address"):
                all_addresses.append(fields["address"])

        
        years = []
        for dob in all_dobs:
            try:
                
                year = int(dob.split("/")[-1])
                years.append(year)
            except Exception:
                continue

        
        address_counts = Counter(all_addresses)
        most_common_address = address_counts.most_common(1)[0][0] if address_counts else None
        dob_range = (min(years), max(years)) if years else (None, None)
        avg_year = int(sum(years)/len(years)) if years else None

        
        summary_text = (
            f"Across {len(extracted_fields_list)} forms, "
            f"the applicants include: {', '.join(all_names)}. "
            f"The most common city is {most_common_address}. "
            f"The birth years range from {dob_range[0]} to {dob_range[1]}, "
            f"with an average year of birth around {avg_year}."
        )

        
        holistic_summary = self.summarizer.summarize(summary_text)

        return {
            "total_forms": len(extracted_fields_list),
            "most_common_city": most_common_address,
            "dob_range": dob_range,
            "average_year": avg_year,
            "all_names": all_names,
            "all_addresses": all_addresses,
            "holistic_summary": holistic_summary
        }
