# Argparse CLI

## Question

How do I build a tiny Python command-line tool with `argparse` and test its core behavior with pytest?

## Run

```powershell
cd D:\Workarea\StudyBook\nuggets
..\env_setter.ps1
python .\python\002_argparse_cli\demo.py
python .\python\002_argparse_cli\demo.py --name Sean --repeat 3 --uppercase
python -m pytest .\python\002_argparse_cli\
```

## Expected Output

- Default run prints one line: `Hello, nuggets!`
- Custom run prints three uppercase lines: `HELLO, SEAN!`
- Pytest reports `3 passed`

## Lesson

How to separate CLI parsing from reusable logic so behavior is easy to test without shelling out.
