# Copyright (c) 2023 Genome Research Ltd.
#
# Authors:
#  Kieron Taylor <kt19@sanger.ac.uk>
#
# This file is part of npg_langqc.
#
# npg_langqc is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, List

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from lang_qc.db.qc_schema import QcState as QcStateDb
from lang_qc.db.qc_schema import QcStateDict, QcType, SeqProduct, User
from lang_qc.models.qc_state import QcState


class BulkQcFetch(BaseModel):

    session: Session = Field(
        title="SQLAlchemy Session",
        description="A SQLAlchemy Session for the LangQC database",
    )

    class Config:
        arbitrary_types_allowed = True

    def query_by_id_list(
        self, ids: List, sequencing_outcomes_only: bool = False
    ) -> Dict[str, list[QcState]]:
        """
        Returns a dictionary whose keys are the given product IDs,
        and the values are lists of QcState records of any type
        for the same product.

        If only sequencing type QC states are required, an optional
        argument, sequencing_outcomes_only, should be set to True.

        Product IDs for which no QC states are available are omitted
        from the response. The response may be an empty dictionary.
        """

        seq_prods = self.get_qc_state_by_id_list(ids)
        return self.extract_qc(
            seq_products=seq_prods, sequencing_outcomes_only=sequencing_outcomes_only
        )

    def get_qc_state_by_id_list(self, ids) -> List[SeqProduct]:
        """
        Generates and executes a query for SeqProducts from a list
        of product IDs. Prefetch all related QC states.
        """
        query = (
            select(SeqProduct)
            .join(QcStateDb)
            .join(QcType)
            .join(QcStateDict)
            .join(User)
            .where(SeqProduct.id_product.in_(ids))
            .options(
                selectinload(SeqProduct.qc_state).options(
                    selectinload(QcStateDb.qc_type),
                    selectinload(QcStateDb.user),
                    selectinload(QcStateDb.qc_state_dict),
                )
            )
        )

        return self.session.execute(query).scalars().all()

    def extract_qc(
        self, seq_products: List[SeqProduct], sequencing_outcomes_only: bool = False
    ) -> Dict[str, Dict[str, QcState]]:
        """
        Given a list of SeqProducts, convert all related QC states into
        QcState response format and hashes them by their product ID.

        If only sequencing type QC states are required, an optional
        argument, sequencing_outcomes_only, should be set to True.
        """
        response = dict()
        for product in seq_products:
            response[product.id_product] = []
            for qc in product.qc_state:
                if sequencing_outcomes_only and (qc.qc_type.qc_type != "sequencing"):
                    pass
                response[product.id_product].append(QcState.from_orm(qc))

        return response
