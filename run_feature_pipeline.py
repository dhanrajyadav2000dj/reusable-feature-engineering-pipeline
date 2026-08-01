from src.config import load_config
from src.pipeline import run_pipeline


def main() -> None:
    config = load_config()
    result = run_pipeline(config)
    print(f"Created {len(result['feature_names'])} features.")
    print("Wrote data/processed/feature_ready_train.csv")
    print("Wrote data/processed/feature_ready_test.csv")
    print("Wrote reports/validation_report.md")
    print("Wrote reports/feature_dictionary.md")
    print("Wrote reports/leakage_review.md")


if __name__ == "__main__":
    main()
