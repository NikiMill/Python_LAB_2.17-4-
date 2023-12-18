#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import click


@click.group()
def cli():
    pass


@cli.command("add")
@click.argument("filename")
@click.option("-n", "--name")
@click.option("-no", "--nomer", type=int)
@click.option("-t", "--time")
def add(filename, name, nomer, time):
    """
    Добавить данные о поезде
    """
    # Запросить данные о поезде.
    poezd = load_poezd(filename)
    poezd.append(
        {
            "nomer": nomer,
            "name": name,
            "time": time,
        }
    )
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(poezd, fout, ensure_ascii=False, indent=4)
    click.secho("Поезд добавлен")


@cli.command("display")
@click.argument("filename")
@click.option("--select", "-s", type=int)
def display(filename, select):
    print(select)
    # Заголовок таблицы.
    poezd = load_poezd(filename)

    if select:
        poezd = selected(poezd, select)

    line = "+-{}-+-{}-+-{}-+".format(
        "-" * 10,
        "-" * 30,
        "-" * 20,
    )
    print(line)
    print("| {:^10} | {:^30} | {:^20} |".format("№", "Пункт назначения", "Время"))
    print(line)

    # Вывести данные о всех поездах.
    for idx, po in enumerate(poezd, 1):
        print(
            "| {:>10} | {:<30} | {:<20} | ".format(
                po.get("nomer", ""), po.get("name", ""), po.get("time", 0)
            )
        )
    print(line)


def selected(list, nom):
    # Проверить сведения поездов из списка.
    poezd = []
    for po in list:
        if po["nomer"] == nom:
            poezd.append(po)
    return poezd


def load_poezd(filename):
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


if __name__ == "__main__":
    cli()
