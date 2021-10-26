import typer
from pprint import pprint
from yachalk import chalk
from genanki import Deck, Package, Card, Note, Model
from textwrap3 import wrap

from models import AnswerPredictor, BooleanQuestion, QuestionGenerator
from summarizer import summarizer
from deck import anki_model

import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = typer.Typer()


@app.command("Generate a list of questions for a specific set of provided text.")
def questions(
    payload,
    question_type=typer.Option(
        default="mcq", prompt="Model type?", help="List of models for question type."
    ),
    summarize_q=typer.Option(
        default="n",
        prompt="Summarize text? [y/n]",
        help="Use machine learning to shorten the input prompt with a summary",
    ),
    question_num: str = typer.Option(
        default=3,
        prompt="How many questions?",
        help="The number of questions generated (might be less if summarizing)",
    ),
):

    my_deck = Deck(2059400110, "Sample")

    if summarize_q == "y":
        payload = summarizer(payload)

    if question_type == "mcq":
        qg = QuestionGenerator()
        output = qg.predict_mcq(payload, question_num)
        typer.echo(chalk.blue(f"Generation took {output['time_taken']:.2f} seconds"))
    elif question_type == "shortq":
        qg = QuestionGenerator()
        output = qg.predict_shortq(payload, question_num)
    else:
        typer.echo("Invalid model type")
        raise typer.Exit()

    typer.echo("text: " + chalk.magenta.italic(wrap(payload, 150)))

    typer.echo("summary: " + chalk.magenta.italic(wrap(summarizer(payload), 150)))

    for question in output["questions"]:
        context = question.get("context")
        question_statement = question.get("question_statement")
        answer = question.get("answer")

        typer.echo(chalk.red("context: ") + context)
        typer.echo(chalk.red("question: ") + question_statement)
        typer.echo(chalk.red("answer: ") + answer)

        sufficient_question = typer.confirm(
            chalk.yellow("Is the question or answer sufficient?")
        )
        if not sufficient_question:
            discard_question = typer.confirm(
                chalk.yellow("Would you like to reword the question or answer?")
            )

            if not discard_question:
                typer.echo("Skipping question")
                continue

            question_statement = typer.prompt(
                chalk.green("Input new question"), default=question_statement
            )
            answer = typer.prompt(chalk.green("Input new answer"), default=answer)

        my_note = Note(model=anki_model, fields=[question_statement, answer])

        my_deck.add_note(my_note)

    Package(my_deck).write_to_file("output.apkg")


if __name__ == "__main__":
    app()
