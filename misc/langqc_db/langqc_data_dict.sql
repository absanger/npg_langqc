-- Dictionaries

insert into seq_platform_dict (`name`, `description`) values
  ('PacBio', 'Pacific Biosciences'),
  ('ONT', 'Oxford Nanopore Technologies'),
  ('Illumina', 'Illumina');

insert into sub_product_attr (`attr_name`, `description`)
  values ('run_name', 'The name of the PacBio run according to LIMS'),
  ('well_label', 'PacBio well (or cell) label'),
  ('flowcell_id', 'ONT flowcell id as recorded by the instrument'),
  ('run_id', 'Run id as generated by the ONT instrument'),
  ('id_run', 'Run id in the NPG run tracking system'),
  ('position', 'Illumina flowcell position (lane)');

insert into user (`username`) values ('user1'), ('user2');

insert into qc_type_dict (`qc_type`, `description`) values
  ('library', 'Sample/library evaluation'),
  ('sequencing', 'Sequencing/instrument evaliation');

insert into qc_outcome_dict (`outcome`, `short_outcome`)
  values ('Passed', 1),
         ('Failed, reagent problem', 0),
         ('Failed, flowcell problem', 0),
         ('Failed', 0);

insert into status_dict (`description`, `long_description`, `temporal_index`)
  values ('qc in progress', 'QC in progress', 100),
         ('qc on hold', 'QC on hold, resolving problems', 120),
         ('manual qc complete', 'Manual QC has been completed', 140),
         ('robo qc complete', 'Robo QC has been completed', 160);
