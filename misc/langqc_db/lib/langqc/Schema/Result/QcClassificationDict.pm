use utf8;
package langqc::Schema::Result::QcClassificationDict;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

langqc::Schema::Result::QcClassificationDict

=cut

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
extends 'DBIx::Class::Core';

=head1 COMPONENTS LOADED

=over 4

=item * L<DBIx::Class::InflateColumn::DateTime>

=back

=cut

__PACKAGE__->load_components("InflateColumn::DateTime");

=head1 TABLE: C<qc_classification_dict>

=cut

__PACKAGE__->table("qc_classification_dict");

=head1 ACCESSORS

=head2 id_qc_classification_dict

  data_type: 'integer'
  extra: {unsigned => 1}
  is_auto_increment: 1
  is_nullable: 0

=head2 description

  data_type: 'varchar'
  is_nullable: 0
  size: 200

=cut

__PACKAGE__->add_columns(
  "id_qc_classification_dict",
  {
    data_type => "integer",
    extra => { unsigned => 1 },
    is_auto_increment => 1,
    is_nullable => 0,
  },
  "description",
  { data_type => "varchar", is_nullable => 0, size => 200 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id_qc_classification_dict>

=back

=cut

__PACKAGE__->set_primary_key("id_qc_classification_dict");

=head1 UNIQUE CONSTRAINTS

=head2 C<unique_qc_category_dict>

=over 4

=item * L</description>

=back

=cut

__PACKAGE__->add_unique_constraint("unique_qc_category_dict", ["description"]);

=head1 RELATIONS

=head2 qc_outcome_hists

Type: has_many

Related object: L<langqc::Schema::Result::QcOutcomeHist>

=cut

__PACKAGE__->has_many(
  "qc_outcome_hists",
  "langqc::Schema::Result::QcOutcomeHist",
  {
    "foreign.id_qc_classification_dict" => "self.id_qc_classification_dict",
  },
  { cascade_copy => 0, cascade_delete => 0 },
);

=head2 qc_outcomes

Type: has_many

Related object: L<langqc::Schema::Result::QcOutcome>

=cut

__PACKAGE__->has_many(
  "qc_outcomes",
  "langqc::Schema::Result::QcOutcome",
  {
    "foreign.id_qc_classification_dict" => "self.id_qc_classification_dict",
  },
  { cascade_copy => 0, cascade_delete => 0 },
);


# Created by DBIx::Class::Schema::Loader v0.07049 @ 2022-06-10 12:17:34
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:HIAhhBrf0N8h+pYLgDuhPw


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;