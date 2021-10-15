import typer
from pprint import pprint
from yachalk import chalk


from models import AnswerPredictor, BoolQGen, QGen

app = typer.Typer()


@app.command("Generate a list of questions for a specific set of provided text.")
def questions(
    payload,
    question_type=typer.Option(
        default="mcq", 
        prompt="Model type?", 
        help="List of models for question type."
    ),
    question_num: str = typer.Option(
        default=3,
        prompt="How many questions?",
        help="The number of questions generated for the provided text.",
    ),
):

    if question_type == "mcq":
        qg = QGen()
        output = qg.predict_mcq(payload, question_num)
        typer.echo(chalk.blue(f"Generation took {output['time_taken']:.2f} seconds"))
    elif question_type == "shortq":
        qg = QGen()
        output = qg.predict_shortq(payload, question_num)
    else:
        typer.echo("Invalid model type")
        raise typer.Exit()

    for question in output["questions"]:
        for (k, v) in question.items():
            print(f"{chalk.red(k)}: {v}")
        print("\n")


if __name__ == "__main__":
    app()
