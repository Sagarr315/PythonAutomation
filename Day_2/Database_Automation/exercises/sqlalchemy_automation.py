
from decimal import Decimal

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Numeric,
    select,
    update,
    delete,
    func,
    URL
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)

from sqlalchemy.exc import SQLAlchemyError

from Database_Automation.config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


# --------------------------------------------------
# 1. DATABASE ENGINE AND CONNECTION POOL
# --------------------------------------------------

database_url = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(
    database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# --------------------------------------------------
# 2. ORM BASE MODEL
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


# --------------------------------------------------
# 3. CREATE EMPLOYEE MODEL
# --------------------------------------------------

class SQLAlchemyEmployee(Base):

    __tablename__ = "sqlalchemy_demo_employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100)
    )

    salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )


# --------------------------------------------------
# 4. CREATE DATABASE TABLES
# --------------------------------------------------

def create_tables():

    Base.metadata.create_all(engine)

    print("SQLAlchemy tables created successfully!")


# --------------------------------------------------
# 5. ORM INSERT
# --------------------------------------------------

def insert_records():

    employees = [

        {
            "name": "Alice",
            "email": "alice.orm@example.com",
            "department": "IT",
            "salary": Decimal("60000.00")
        },

        {
            "name": "Robert",
            "email": "robert.orm@example.com",
            "department": "HR",
            "salary": Decimal("45000.00")
        },

        {
            "name": "David",
            "email": "david.orm@example.com",
            "department": "Finance",
            "salary": Decimal("55000.00")
        }

    ]

    with SessionLocal.begin() as session:

        for employee_data in employees:

            existing = session.scalar(
                select(SQLAlchemyEmployee).where(
                    SQLAlchemyEmployee.email
                    == employee_data["email"]
                )
            )

            if existing is None:

                employee = SQLAlchemyEmployee(
                    **employee_data
                )

                session.add(employee)

                print(
                    "Inserted:",
                    employee_data["email"]
                )

            else:

                print(
                    "Already exists:",
                    employee_data["email"]
                )

    print("ORM insert completed!")


# --------------------------------------------------
# 6. ORM SELECT
# --------------------------------------------------

def fetch_records():

    with SessionLocal() as session:

        employees = session.scalars(
            select(SQLAlchemyEmployee).order_by(
                SQLAlchemyEmployee.id
            )
        ).all()

        print("\n--- ORM EMPLOYEE RECORDS ---")

        for employee in employees:

            print(
                employee.id,
                employee.name,
                employee.email,
                employee.department,
                employee.salary
            )


# --------------------------------------------------
# 7. ORM UPDATE
# --------------------------------------------------

def update_record():

    with SessionLocal.begin() as session:

        employee = session.scalar(
            select(SQLAlchemyEmployee).where(
                SQLAlchemyEmployee.email
                == "alice.orm@example.com"
            )
        )

        if employee is not None:

            employee.salary = Decimal("75000.00")

            employee.department = "Technology"

            print("\nORM employee updated!")

        else:

            print("Employee not found!")


# --------------------------------------------------
# 8. ORM AGGREGATE FUNCTIONS
# --------------------------------------------------

def aggregate_records():

    with SessionLocal() as session:

        total_employees = session.scalar(
            select(func.count(SQLAlchemyEmployee.id))
        )

        average_salary = session.scalar(
            select(func.avg(SQLAlchemyEmployee.salary))
        )

        total_salary = session.scalar(
            select(func.sum(SQLAlchemyEmployee.salary))
        )

        print("\n--- ORM AGGREGATE RESULTS ---")

        print("Total Employees:", total_employees)

        print("Average Salary:", average_salary)

        print("Total Salary:", total_salary)


# --------------------------------------------------
# 9. SQLALCHEMY CORE OPERATIONS
# --------------------------------------------------

def core_operations():

    employee_table = SQLAlchemyEmployee.__table__

    with engine.begin() as connection:

        # Core INSERT
        existing = connection.execute(
            select(employee_table.c.id).where(
                employee_table.c.email
                == "core.demo@example.com"
            )
        ).first()

        if existing is None:

            connection.execute(
                employee_table.insert().values(
                    name="Core User",
                    email="core.demo@example.com",
                    department="Operations",
                    salary=Decimal("50000.00")
                )
            )

            print("\nCore insert completed!")

        # Core SELECT
        result = connection.execute(
            select(employee_table).where(
                employee_table.c.department
                == "Operations"
            )
        )

        print("\n--- CORE SELECT ---")

        for row in result.mappings():
            print(dict(row))

        # Core UPDATE
        result = connection.execute(
            update(employee_table)
            .where(
                employee_table.c.email
                == "core.demo@example.com"
            )
            .values(
                salary=Decimal("55000.00")
            )
        )

        print("\nCore update affected:", result.rowcount)


# --------------------------------------------------
# 10. ORM DELETE
# --------------------------------------------------

def delete_record():

    with SessionLocal.begin() as session:

        employee = session.scalar(
            select(SQLAlchemyEmployee).where(
                SQLAlchemyEmployee.email
                == "robert.orm@example.com"
            )
        )

        if employee is not None:

            session.delete(employee)

            print("\nORM delete completed!")

        else:

            print("Delete target not found!")


# --------------------------------------------------
# 11. CORE DELETE
# --------------------------------------------------

def core_delete():

    employee_table = SQLAlchemyEmployee.__table__

    with engine.begin() as connection:

        result = connection.execute(
            delete(employee_table).where(
                employee_table.c.email
                == "core.demo@example.com"
            )
        )

        print(
            "\nCore delete affected:",
            result.rowcount
        )


# --------------------------------------------------
# 12. CONNECTION POOL INFORMATION
# --------------------------------------------------

def connection_pool_info():

    print("\n--- CONNECTION POOL ---")

    print(engine.pool.status())


# --------------------------------------------------
# 13. MAIN EXECUTION
# --------------------------------------------------

def run_automation():

    try:

        with engine.connect() as connection:

            connection.execute(select(1))

        print("SQLAlchemy MySQL connection successful!")

        create_tables()

        insert_records()

        fetch_records()

        update_record()

        aggregate_records()

        core_operations()

        delete_record()

        core_delete()

        fetch_records()

        connection_pool_info()

        print("\nSQLAlchemy automation completed!")

    except SQLAlchemyError as error:

        print("SQLAlchemy Database Error:", error)

    except Exception as error:

        print("Execution Error:", error)

    finally:

        engine.dispose()

        print("SQLAlchemy connections disposed!")


if __name__ == "__main__":
    run_automation()
