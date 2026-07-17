from app.preprocessing.processor_pipeline import ProcessorPipeline

pipeline = ProcessorPipeline(
    "data/raw/metadata/metadata.csv"
)

pipeline.run()