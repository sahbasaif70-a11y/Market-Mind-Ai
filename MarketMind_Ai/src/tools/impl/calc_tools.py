from typing import List, Dict, Any

def calculate_metric(metric_type: str, values: List[float]) -> Dict[str, Any]:
    """Calculate statistical or financial metrics."""
    if not values:
        return {"status": "error", "message": "No numerical values provided for calculation."}

    try:
        if metric_type == "average":
            result = sum(values) / len(values)
            return {"status": "success", "metric": "average", "result": round(result, 4)}

        elif metric_type == "sum":
            result = sum(values)
            return {"status": "success", "metric": "sum", "result": round(result, 4)}

        elif metric_type == "growth_rate":
            if len(values) < 2:
                return {"status": "error", "message": "Growth rate calculation requires at least 2 values (start, end)."}
            start_val, end_val = values[0], values[-1]
            if start_val == 0:
                return {"status": "error", "message": "Starting value cannot be 0 for growth rate."}
            growth = ((end_val - start_val) / start_val) * 100
            return {"status": "success", "metric": "growth_rate_percent", "result": round(growth, 2)}

        elif metric_type == "cagr":
            # CAGR = (End Value / Start Value)^(1 / periods) - 1
            if len(values) < 2:
                return {"status": "error", "message": "CAGR requires at least start value and end value."}
            start_val, end_val = values[0], values[-1]
            periods = len(values) - 1
            if start_val <= 0 or periods <= 0:
                return {"status": "error", "message": "Invalid values or periods for CAGR."}
            cagr = ((end_val / start_val) ** (1 / periods) - 1) * 100
            return {"status": "success", "metric": "cagr_percent", "result": round(cagr, 2)}

        else:
            return {"status": "error", "message": f"Unsupported metric_type: '{metric_type}'."}

    except Exception as e:
        return {"status": "error", "message": f"Calculation error: {str(e)}"}
