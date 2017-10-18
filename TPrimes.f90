program primes
    implicit none
!    integer, parameter  :: N = 1000
    integer             :: p, m, i
    logical, allocatable :: is_p(:)
    integer, allocatable :: p_list(:)

    print*,"enter maximum integer"
    read (*,*)p
    allocate(is_p(p))
    call sieve(is_p, p)
    m = 0
    do i=1,p
        if (is_p(i)) then
            m = m + 1
        end if
    end do
    print*, "Found ", m, " primes < ", p
    allocate(p_list(m))
    call logical_to_integer(p_list, is_p, m, p)

    write (*,'(100I5)') (p_list(i), i=1,m)
end program


subroutine sieve(is_prime, n_max)
! =====================================================
! Uses the sieve of Eratosthenes to compute a logical
! array of size n_max, where .true. in element i
! indicates that i is a prime.
! =====================================================
    integer, intent(in)   :: n_max
    logical, intent(out)  :: is_prime(n_max)
    integer :: i
    is_prime = .true.
    is_prime(1) = .false.
    do i = 2, int(sqrt(real(n_max)))
        if (is_prime (i)) is_prime (i * i : n_max : i) = .false.
    end do
    return
end subroutine

subroutine logical_to_integer(prime_numbers, is_prime, num_primes, n)
! =====================================================
! Translates the logical array from sieve to an array
! of size num_primes of prime numbers.
! =====================================================
    integer                 :: i, j=0
    integer, intent(in)     :: n
    integer, intent(in)     :: num_primes
    logical, intent(in)     :: is_prime(n)
    integer, intent(out)    :: prime_numbers(num_primes)
!    integer, intent(out), dimension(0:num_primes-1) :: prime_numbers
    do i = 1, size(is_prime)
        if (is_prime(i)) then
            j = j + 1
            prime_numbers(j) = i
        end if
    end do
end subroutine
