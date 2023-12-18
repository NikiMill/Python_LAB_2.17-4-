#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Использовать словарь, содержащий следующиек лючи: название пунктa аназначения; номерпоезда; времяотправления.
#Написать программу, выполняющую следующие действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры; записи должны быть упорядочены по номерам поездов;
#необходимо реализовать интерфейс командной строки (CLI).
import argparse
import json
import os.path


def get_train(train, name, no, time):

    train.append({"name": name, "no": no, "time": time})
    return train


def list(train):
    if train:
        line = "+-{}-+-{}-+-{}-+".format(
            "-" * 10,
            "-" * 20,
            "-" * 8,
        )
        print(line)
        print("| {:^10} | {:^20} | {:^8} |".format(" No ", "Название", "Время"))
        print(line)

        for idx, po in enumerate(train, 1):
            print(
                "| {:>10} | {:<20} | {"
                "} |".format(po.get("no", ""), po.get("name", ""), po.get("time", ""))
            )
        print(line)

    else:
        print("Список поездов пуст.")


def select_train(train, nom):
    rezult = []
    for idx, po in enumerate(train, 1):
        if po["no"] == str(nom):
            rezult.append(po)

    return rezult


def save_train(file_name, train):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(train, fout, ensure_ascii=False, indent=4)


def load_train(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="Имя файла данных")

    parser = argparse.ArgumentParser("train")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", parents=[file_parser], help="Добавить поезд")
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="Название пункта назначения?",
    )
    add.add_argument("--no", action="store", type=int, help="Номер поезда?")
    add.add_argument(
        "-t", "--time", action="store", required=True, help="Время отправления?"
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Панель отображения поездов"
    )

    select = subparsers.add_parser(
        "select", parents=[file_parser], help="Выбор поезда по номеру"
    )
    select.add_argument(
        "-o",
        "--nom",
        action="store",
        type=int,
        required=True,
        help="Введите номер поезда",
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        train = load_train(args.filename)
    else:
        train = []

    if args.command == "add":
        train = get_train(train, args.name, args.no, args.time)
        is_dirty = True

    elif args.command == "display":
        list(train)

    elif args.command == "select":
        selected = select_train(train, args.nom)
        list(selected)

    if is_dirty:
        save_train(args.filename, train)


if __name__ == "__main__":
    main()
