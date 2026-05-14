type Props = {
  page: number;
  perPage: number;
  totalCount: number;
  onPageChange: (page: number) => void;
};

export function PaginationControls({ page, perPage, totalCount, onPageChange }: Props) {
  const totalPages = Math.max(1, Math.ceil(totalCount / perPage));

  return (
    <div className="row">
      <button className="button secondary" disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
        Previous
      </button>
      <span className="muted">
        Page {page} of {totalPages} ({totalCount} jobs)
      </span>
      <button
        className="button secondary"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
}
