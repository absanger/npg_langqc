use utf8;
package langqc::Schema::Result::ProductAnnotation;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

langqc::Schema::Result::ProductAnnotation

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

=head1 TABLE: C<product_annotation>

=cut

__PACKAGE__->table("product_annotation");

=head1 ACCESSORS

=head2 id_product_annotation

  data_type: 'bigint'
  extra: {unsigned => 1}
  is_auto_increment: 1
  is_nullable: 0

=head2 id_annotation

  data_type: 'bigint'
  extra: {unsigned => 1}
  is_foreign_key: 1
  is_nullable: 0

=head2 id_seq_product

  data_type: 'bigint'
  extra: {unsigned => 1}
  is_foreign_key: 1
  is_nullable: 0

=cut

__PACKAGE__->add_columns(
  "id_product_annotation",
  {
    data_type => "bigint",
    extra => { unsigned => 1 },
    is_auto_increment => 1,
    is_nullable => 0,
  },
  "id_annotation",
  {
    data_type => "bigint",
    extra => { unsigned => 1 },
    is_foreign_key => 1,
    is_nullable => 0,
  },
  "id_seq_product",
  {
    data_type => "bigint",
    extra => { unsigned => 1 },
    is_foreign_key => 1,
    is_nullable => 0,
  },
);

=head1 PRIMARY KEY

=over 4

=item * L</id_product_annotation>

=back

=cut

__PACKAGE__->set_primary_key("id_product_annotation");

=head1 RELATIONS

=head2 annotation

Type: belongs_to

Related object: L<langqc::Schema::Result::Annotation>

=cut

__PACKAGE__->belongs_to(
  "annotation",
  "langqc::Schema::Result::Annotation",
  { id_annotation => "id_annotation" },
  { is_deferrable => 1, on_delete => "NO ACTION", on_update => "NO ACTION" },
);

=head2 seq_product

Type: belongs_to

Related object: L<langqc::Schema::Result::SeqProduct>

=cut

__PACKAGE__->belongs_to(
  "seq_product",
  "langqc::Schema::Result::SeqProduct",
  { id_seq_product => "id_seq_product" },
  { is_deferrable => 1, on_delete => "NO ACTION", on_update => "NO ACTION" },
);


# Created by DBIx::Class::Schema::Loader v0.07049 @ 2022-06-08 17:39:30
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:oUm5DQT+krZHjYB3BXlhDQ


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;