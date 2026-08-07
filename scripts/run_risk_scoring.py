from app.analytics.risk_scoring import RiskScoring

def main():
    
    print("=" * 60)
    print("Supply Chain Intelligence Platform")
    print("Risk Scoring")
    print("=" * 60)
    
    scorer = RiskScoring()
    
    try:
        # =====================================================
        # Run Risk Scoring pipeline
        # =====================================================
        
        scorer.run()
        
        # =====================================================
        # Display Risk Scores Results
        # =====================================================
        
        print("\nTop Risk Entities")
        print("-" * 120)
        
        print(
            f"{'Name':<30}"
            f"{'Type':<20}"
            f"{'Risk Score':<12}"
            f"{'Risk Level':<12}"
            f"{'Degree':<10}"
            f"{'Betweenness':<15}"
            f"{'Closeness':<12}"
        )
        
        print("-" * 120)
        
        rows = scorer.top_risky_entities(limit=20)
        
        for row in rows:
            
            print(
                f"{row['name']:<30}"
                f"{row['type']:<20}"
                f"{row['risk_score']:<12.4f}"
                f"{row['risk_level']:<12}"
                f"{row['degree']:<10}"
                f"{row['betweenness']:<15}"
                f"{row['closeness']:<12}"
            )
            
        print("\n" + "=" * 60)
        print("Risk scoring completed successfully.")
        print("=" * 60)
        
    except Exception as error:
        
        print("\n" + "="  * 60)
        print("Risk Scoring Failed")
        print("=" * 60)
        print(f"Error: {error}")
    
    finally:
        
        scorer.close()
        
if __name__ == "__main__":
    main()
              
                                        